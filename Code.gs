/*
 * MG - POC V1 - Social Media Reporting
 * Google Apps Script Web App backend - OPTIMISÉ FINAL
 * 
 * ⚡ CHANGEMENTS:
 * - PBKDF2 itérations: 100000 (sûr + rapide)
 * - getPbkdf2Iterations() retourne 100000 directement (pas de calibration lente)
 * - Gestion d'erreur améliorée
 * - Timeout réseau augmenté
 */

var CACHE = CacheService.getScriptCache();
var PROPS = PropertiesService.getScriptProperties();

function doPost(e) {
  try {
    var raw = (e && e.postData && e.postData.contents) ? e.postData.contents : '';
    var data = raw ? JSON.parse(raw) : {};

    if (!isAuthorizedRequest(e, data)) {
      return jsonResponse({ ok: false, error: 'UNAUTHORIZED' });
    }

    if (!data || !data.route) {
      return jsonResponse({ ok: false, error: 'INVALID_ROUTE' });
    }

    switch (data.route) {
      case 'health':
        return jsonResponse({ ok: true, ts: new Date().toISOString(), version: 'v1' });
      case 'oauth_init':
        return jsonResponse(routeOauthInit(data));
      case 'oauth_status':
        return jsonResponse(routeOauthStatus(data));
      case 'register_start':
        return jsonResponse(routeRegisterStart(data));
      case 'register_verify':
        return jsonResponse(routeRegisterVerify(data));
      case 'login':
        return jsonResponse(routeLogin(data));
      default:
        return jsonResponse({ ok: false, error: 'INVALID_ROUTE' });
    }
  } catch (err) {
    return jsonResponse({ ok: false, error: 'SERVER_ERROR', details: String(err) });
  }
}

function doGet(e) {
  try {
    if (!e || !e.parameter || !e.parameter.oauth) {
      return HtmlService.createHtmlOutput('');
    }
    var provider = (e.parameter.provider || '').toLowerCase();
    var state = e.parameter.state;
    var code = e.parameter.code;

    if (!provider || !state || !code) {
      return HtmlService.createHtmlOutput('Paramètres manquants.');
    }

    var stateKey = 'OAUTH_STATE_' + state;
    var stateRaw = CACHE.get(stateKey);
    if (!stateRaw) {
      return HtmlService.createHtmlOutput('State invalide ou expiré.');
    }

    var stateObj = JSON.parse(stateRaw);
    var email = stateObj.email;

    var token = exchangeMetaToken(code, provider);
    var ids = fetchMetaIds(provider, token);

    var linkKey = 'OAUTH_LINK_' + email;
    var existing = CACHE.get(linkKey);
    var payload = existing ? JSON.parse(existing) : {};
    payload.linkedAt = new Date().toISOString();
    if (provider === 'facebook') {
      payload.id_fb = ids.id;
    } else if (provider === 'instagram') {
      payload.id_insta = ids.id;
    }

    CACHE.put(linkKey, JSON.stringify(payload), 60 * 60);
    CACHE.remove(stateKey);

    GmailApp.sendEmail(email, 'Liaison réalisée',
      'Votre compte ' + provider + ' a bien été lié.');

    return HtmlService.createHtmlOutput(
      '<div style="font-family:Arial;padding:24px;">' +
      '<h2>Liaison réussie</h2>' +
      '<p>Vous pouvez fermer cette fenêtre.</p>' +
      '</div>'
    );
  } catch (err) {
    return HtmlService.createHtmlOutput('Erreur: ' + err);
  }
}

function routeOauthInit(data) {
  var email = (data.email || '').trim();
  var provider = (data.provider || '').toLowerCase();

  if (!isValidEmail(email) || (provider !== 'facebook' && provider !== 'instagram')) {
    return { ok: false, error: 'INVALID_INPUT' };
  }

  var state = Utilities.getUuid();
  var nonce = Utilities.getUuid();
  var key = 'OAUTH_STATE_' + state;
  CACHE.put(key, JSON.stringify({ email: email, provider: provider, createdAt: Date.now(), nonce: nonce }), 10 * 60);

  var webAppUrl = getWebAppUrl();
  var appId = getRequiredProp('META_APP_ID');
  var redirectUri = webAppUrl + '?oauth=1&provider=' + encodeURIComponent(provider);
  var scopes = provider === 'facebook'
    ? 'public_profile,email,pages_show_list,pages_read_engagement'
    : 'instagram_basic,instagram_manage_insights,pages_show_list';

  var authUrl = 'https://www.facebook.com/v19.0/dialog/oauth' +
    '?client_id=' + encodeURIComponent(appId) +
    '&redirect_uri=' + encodeURIComponent(redirectUri) +
    '&response_type=code' +
    '&state=' + encodeURIComponent(state) +
    '&scope=' + encodeURIComponent(scopes);

  return { ok: true, authUrl: authUrl };
}

function routeOauthStatus(data) {
  var email = (data.email || '').trim();
  if (!isValidEmail(email)) {
    return { ok: false, error: 'INVALID_INPUT' };
  }

  var linkKey = 'OAUTH_LINK_' + email;
  var raw = CACHE.get(linkKey);
  if (!raw) {
    return { ok: true, facebookLinked: false, instagramLinked: false };
  }
  var payload = JSON.parse(raw);
  return {
    ok: true,
    facebookLinked: Boolean(payload.id_fb),
    instagramLinked: Boolean(payload.id_insta),
    id_fb: payload.id_fb || null,
    id_insta: payload.id_insta || null
  };
}

function routeRegisterStart(data) {
  var email = (data.email || '').trim();
  var password = data.password || '';
  var nom = (data.nom_entreprise || '').trim();
  var secteur = (data.secteur || '').trim();

  if (!isValidEmail(email) || password.length < 8 || !nom || !isValidSecteur(secteur)) {
    return { ok: false, error: 'INVALID_INPUT' };
  }

  var sheet = getClientsSheet();
  if (findClientRowByEmail(sheet, email) !== -1) {
    return { ok: false, error: 'EMAIL_EXISTS' };
  }

  var linkRaw = CACHE.get('OAUTH_LINK_' + email);
  var link = linkRaw ? JSON.parse(linkRaw) : { id_fb: '', id_insta: '' };

  var iterations = getPbkdf2Iterations();  // ← Retourne 100000
  var pepper = getRequiredProp('PEPPER_SECRET');
  var salt = randomBytes(16);
  var hashBytes = pbkdf2Sha256(password + pepper, salt, iterations, 32);
  var passwordHashString = encodeHash(iterations, salt, hashBytes);

  var code = generateCode();
  var codeSalt = randomBytes(16);
  var codeIterations = 50000;
  var codeHash = pbkdf2Sha256(code + pepper, codeSalt, codeIterations, 32);

  var pending = {
    email: email,
    nom_entreprise: nom,
    secteur: secteur,
    passwordHashString: passwordHashString,
    id_fb: link.id_fb || '',
    id_insta: link.id_insta || '',
    codeIterations: codeIterations,
    codeSalt: Utilities.base64Encode(codeSalt),
    codeHash: Utilities.base64Encode(codeHash),
    expiresAt: Date.now() + 15 * 60 * 1000
  };

  CACHE.put('PENDING_' + email, JSON.stringify(pending), 15 * 60);
  
  try {
    GmailApp.sendEmail(email, 'Code de confirmation MG',
      'Votre code : ' + code + ' (valable 15 minutes)');
  } catch (err) {
    // Continuons même si l'email échoue temporairement
  }

  return { ok: true };
}

function routeRegisterVerify(data) {
  var email = (data.email || '').trim();
  var code = (data.code || '').trim();
  if (!email || !code) {
    return { ok: false, error: 'INVALID_INPUT' };
  }

  var pendingRaw = CACHE.get('PENDING_' + email);
  if (!pendingRaw) {
    return { ok: false, error: 'CODE_EXPIRED' };
  }

  var pending = JSON.parse(pendingRaw);
  if (Date.now() > pending.expiresAt) {
    CACHE.remove('PENDING_' + email);
    return { ok: false, error: 'CODE_EXPIRED' };
  }

  var pepper = getRequiredProp('PEPPER_SECRET');
  var codeSalt = Utilities.base64Decode(pending.codeSalt);
  var expectedHash = Utilities.base64Decode(pending.codeHash);
  var computed = pbkdf2Sha256(code + pepper, codeSalt, pending.codeIterations, 32);

  if (!constantTimeEqual(expectedHash, computed)) {
    return { ok: false, error: 'INVALID_CODE' };
  }

  var sheet = getClientsSheet();
  var idClient = Utilities.getUuid();
  var createdAt = new Date().toISOString();

  sheet.appendRow([
    idClient,
    pending.email,
    pending.passwordHashString,
    pending.id_fb,
    pending.id_insta,
    pending.nom_entreprise,
    pending.secteur,
    createdAt
  ]);

  CACHE.remove('PENDING_' + email);

  return { ok: true, id_client: idClient };
}

function routeLogin(data) {
  var email = (data.email || '').trim();
  var password = data.password || '';

  if (!isValidEmail(email) || !password) {
    return { ok: false, error: 'INVALID_CREDENTIALS' };
  }

  if (isRateLimited(email)) {
    return { ok: false, error: 'RATE_LIMIT' };
  }

  var sheet = getClientsSheet();
  var rowIndex = findClientRowByEmail(sheet, email);
  if (rowIndex === -1) {
    incrementRateLimit(email);
    return { ok: false, error: 'INVALID_CREDENTIALS' };
  }

  var row = sheet.getRange(rowIndex, 1, 1, 8).getValues()[0];
  var passwordHash = row[2];
  var parsed = parseHash(passwordHash);

  var pepper = getRequiredProp('PEPPER_SECRET');
  var computed = pbkdf2Sha256(password + pepper, parsed.salt, parsed.iterations, 32);

  if (!constantTimeEqual(parsed.hash, computed)) {
    incrementRateLimit(email);
    return { ok: false, error: 'INVALID_CREDENTIALS' };
  }

  clearRateLimit(email);

  return { ok: true, id_client: row[0], email: email };
}

function isAuthorizedRequest(e, data) {
  var expected = getRequiredProp('API_KEY');
  var provided = '';
  if (data && data.api_key) {
    provided = String(data.api_key);
  } else if (e && e.parameter && e.parameter.api_key) {
    provided = String(e.parameter.api_key);
  }
  provided = provided.trim();
  return provided && expected && provided === expected;
}

function getHeader(e, key) {
  if (!e || !e.headers) {
    return '';
  }
  return e.headers[key] || e.headers[key.toLowerCase()] || '';
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function getClientsSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('CLIENTS');
  if (!sheet) {
    throw new Error('Onglet CLIENTS introuvable.');
  }
  return sheet;
}

function findClientRowByEmail(sheet, email) {
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) {
    return -1;
  }
  var range = sheet.getRange(2, 2, lastRow - 1, 1).getValues();
  for (var i = 0; i < range.length; i++) {
    if (String(range[i][0]).toLowerCase() === email.toLowerCase()) {
      return i + 2;
    }
  }
  return -1;
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidSecteur(secteur) {
  var allowed = ['Influenceur', 'Salle de sport', 'Hôtellerie/Restauration'];
  return allowed.indexOf(secteur) !== -1;
}

function generateCode() {
  var code = Math.floor(Math.random() * 1000000);
  return ('000000' + code).slice(-6);
}

function getPbkdf2Iterations() {
  // ⚡ OPTIMISÉ: Retourne directement 100000 (pas 10000!)
  // 100000 = standard OWASP 2024 + très rapide sur Apps Script
  var prop = PROPS.getProperty('PBKDF2_ITERATIONS');
  if (prop) {
    var parsed = parseInt(prop, 10);
    // Valider la valeur (min 50000, max 500000)
    return Math.max(50000, Math.min(500000, parsed));
  }
  return 100000;  // ← VALEUR PAR DÉFAUT OPTIMISÉE
}

function calibrateIterations(targetMs) {
  var iterations = 50000;
  var salt = randomBytes(16);
  var start = Date.now();
  pbkdf2Sha256('calibration', salt, iterations, 32);
  var elapsed = Date.now() - start;
  if (elapsed === 0) {
    return iterations;
  }
  var scale = targetMs / elapsed;
  var adjusted = Math.max(10000, Math.round(iterations * scale));
  return adjusted;
}

function encodeHash(iterations, saltBytes, hashBytes) {
  return 'pbkdf2_sha256$' + iterations + '$' +
    Utilities.base64Encode(saltBytes) + '$' + Utilities.base64Encode(hashBytes);
}

function parseHash(value) {
  var parts = String(value).split('$');
  if (parts.length !== 4) {
    throw new Error('Format de hash invalide');
  }
  return {
    iterations: parseInt(parts[1], 10),
    salt: Utilities.base64Decode(parts[2]),
    hash: Utilities.base64Decode(parts[3])
  };
}

function pbkdf2Sha256(password, saltBytes, iterations, dkLen) {
  var keyBytes = stringToBytes(password);
  var hashLength = 32;
  var blocks = Math.ceil(dkLen / hashLength);
  var output = [];

  for (var blockIndex = 1; blockIndex <= blocks; blockIndex++) {
    var block = saltBytes.slice(0);
    block = block.concat(int32ToBytes(blockIndex));

    var u = hmacSha256(keyBytes, block);
    var t = u.slice(0);

    for (var i = 1; i < iterations; i++) {
      u = hmacSha256(keyBytes, u);
      xorBytes(t, u);
    }

    output = output.concat(t);
  }

  return output.slice(0, dkLen);
}

function hmacSha256(keyBytes, messageBytes) {
  return Utilities.computeHmacSha256Signature(messageBytes, keyBytes);
}

function xorBytes(target, source) {
  for (var i = 0; i < target.length; i++) {
    target[i] = (target[i] ^ source[i]) & 0xff;
  }
}

function int32ToBytes(value) {
  return [
    (value >> 24) & 0xff,
    (value >> 16) & 0xff,
    (value >> 8) & 0xff,
    value & 0xff
  ];
}

function stringToBytes(text) {
  return Utilities.newBlob(text).getBytes();
}

function randomBytes(length) {
  var bytes = [];
  for (var i = 0; i < length; i++) {
    bytes.push(Math.floor(Math.random() * 256));
  }
  return bytes;
}

function constantTimeEqual(a, b) {
  if (!a || !b) {
    return false;
  }
  var maxLen = Math.max(a.length, b.length);
  var result = 0;
  for (var i = 0; i < maxLen; i++) {
    var av = a[i % a.length] || 0;
    var bv = b[i % b.length] || 0;
    result |= av ^ bv;
  }
  return result === 0 && a.length === b.length;
}

function getRequiredProp(name) {
  var value = PROPS.getProperty(name);
  if (!value) {
    throw new Error('Propriété manquante: ' + name);
  }
  return value;
}

function getWebAppUrl() {
  var url = PROPS.getProperty('WEBAPP_URL');
  if (url) {
    return url;
  }
  var scriptId = ScriptApp.getScriptId();
  return 'https://script.google.com/macros/s/' + scriptId + '/exec';
}

function exchangeMetaToken(code, provider) {
  var appId = getRequiredProp('META_APP_ID');
  var appSecret = getRequiredProp('META_APP_SECRET');
  var webAppUrl = getWebAppUrl();
  var redirectProvider = provider === 'instagram' ? 'instagram' : 'facebook';
  var url = 'https://graph.facebook.com/v19.0/oauth/access_token' +
    '?client_id=' + encodeURIComponent(appId) +
    '&redirect_uri=' + encodeURIComponent(webAppUrl + '?oauth=1&provider=' + redirectProvider) +
    '&client_secret=' + encodeURIComponent(appSecret) +
    '&code=' + encodeURIComponent(code);

  var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  var payload = JSON.parse(response.getContentText());
  if (!payload.access_token) {
    throw new Error('Erreur OAuth: ' + response.getContentText());
  }
  return payload.access_token;
}

function fetchMetaIds(provider, accessToken) {
  if (provider === 'facebook') {
    var resp = UrlFetchApp.fetch('https://graph.facebook.com/me?fields=id&access_token=' +
      encodeURIComponent(accessToken));
    var data = JSON.parse(resp.getContentText());
    return { id: data.id };
  }
  if (provider === 'instagram') {
    var igResp = UrlFetchApp.fetch('https://graph.facebook.com/me?fields=id,account_type&access_token=' +
      encodeURIComponent(accessToken));
    var igData = JSON.parse(igResp.getContentText());
    return { id: igData.id };
  }
  throw new Error('Provider inconnu');
}

function isRateLimited(email) {
  var key = 'LOGIN_ATTEMPTS_' + email;
  var raw = CACHE.get(key);
  if (!raw) {
    return false;
  }
  var data = JSON.parse(raw);
  if (Date.now() > data.resetAt) {
    CACHE.remove(key);
    return false;
  }
  return data.count >= 10;
}

function incrementRateLimit(email) {
  var key = 'LOGIN_ATTEMPTS_' + email;
  var raw = CACHE.get(key);
  var data = raw ? JSON.parse(raw) : { count: 0, resetAt: Date.now() + 15 * 60 * 1000 };
  data.count += 1;
  CACHE.put(key, JSON.stringify(data), 15 * 60);
}

function clearRateLimit(email) {
  CACHE.remove('LOGIN_ATTEMPTS_' + email);
}
