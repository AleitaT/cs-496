'use strict';

const config = require('./src/config.js');
const logging = require('./src/logging.js');
const log = logging.events;
const db = require('./src/db.js');
const express = require('express');
const app = module.exports = express();
const vhost = require('./src/vhost.js');
const compression = require('compression');

// Disable the X-Powered-By (security reasons)
app.disable('x-powered-by');

// set up template engine
app.set('views', './vhosts/');
app.set('view engine', 'pug');

// Setup access logs
app.use(logging.access);

// If not production then we add no index header
app.use(function(req, res, next) {
  if (process.env.NODE_ENV !== 'production') {
    res.set('X-Robots-Tag', 'noindex');
  }

  return next();
});

// GZIP
app.use(compression());

// GET /ping and EB health check handler
app.use(require('./src/healthcheck.js'));

// If production then check if https, if not redirect
if (config.env === 'production'
  || config.env === 'test'
  || config.env === 'tests') {
  app.use(require('./src/httpsredirect.js'));
}

// Domain lookup. If domain not configured, will return 404
app.use(vhost.handleRequest);

// Bind routes
require('./src/routes.js')(app);

// Check authentication
db.authenticate().then(() => {
  log.info('Success connecting to database: %s', config.db_name);

  // Setup the virtual hosts
  return vhost.setup();
}).then((numVhosts) => {
  log.info('Loaded %d vhosts', numVhosts);

  app._server = app.listen(config.port, (err) => {
    if (err) {
      log.error('Error listening on port: %s', JSON.stringify(err));
      throw err;
    }

    log.info('Started on: %s', config.port);

    // event emitter for testing
    app.emit('ready');
  });
}).catch((err) => {
  log.error('Error starting service: %s', JSON.stringify(err));
  process.exit(1);
});