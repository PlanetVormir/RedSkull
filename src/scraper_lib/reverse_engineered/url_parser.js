function mi(t) {
    var c = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    if ((t = (t = (t = "".concat(t)).replace(/[\t\n\f\r]/g, "")).length % 4 == 0 ? t.replace(/==?$/, "") : t).length % 4 == 1 || /[^+/0-9A-Za-z]/.test(t)) {
        return null;
    }

    for (var i, e = "", u = 0, $ = 0, s = 0; s < t.length; s++) {
        u = (u <<= 6) | (i = t[s],
            (i = c.indexOf(i)) < 0 ? void 0 : i),
        24 === ($ += 6) && (e = (e = (e += String.fromCharCode((16711680 & u) >> 16)) + String.fromCharCode(((65280 & u) >> 8))) + String.fromCharCode(255 & u),
            u = $ = 0);
    }

    return 12 === $ ? (u >>= 4,
        e += String.fromCharCode(u)) : 18 === $ && (u >>= 2,
        e = (e += String.fromCharCode((65280 & u) >> 8)) + String.fromCharCode(255 & u)),
        e
}


function encode(t, n) {
    var S = "";

    for (var i, _ = [], e = 0, o = S, u = 0; u < 256; u++) {
        _[u] = u;
    }
    for (u = 0; u < 256; u++) {
        e = (e + _[u] + t.charCodeAt(u % t.length)) % 256,
            i = _[u],
            _[u] = _[e],
            _[e] = i;
    }
    for (var u = 0, e = 0, c = 0; c < n.length; c++) {
        e = (e + _[u = (u + 1) % 256]) % 256,
            i = _[u],
            _[u] = _[e],
            _[e] = i,
            o += String.fromCharCode(n.charCodeAt(c) ^ _[(_[u] + _[e]) % 256]);
    }
    return o
}

// t is the wierd url
function main(t) {
    return decodeURIComponent(
        encode(
            "DZmuZuXqa9O0z3b7", mi(t)
        )
    )
}

