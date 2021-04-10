// you will need to install via 'npm install jsonwebtoken' or in your package.json

var jwt = require("jsonwebtoken");

var METABASE_SITE_URL = "https://justdance.dei.uc.pt";
var METABASE_SECRET_KEY = "34fa977d001eb28c0e6e551dff101b0396a36f31174334b5366fb19af6eaf8fe";

var payload = {
  resource: { dashboard: 2 },
  params: {},
  exp: Math.round(Date.now() / 1000) + (10 * 60) // 10 minute expiration
};
var token = jwt.sign(payload, METABASE_SECRET_KEY);

var iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true";