/**
 * Veyron landing-page router (Cloudflare Worker).
 * Every *.veyronbiologics.com subdomain → its matching landing page in the veyron-lp repo
 * (served from GitHub Pages). Adding a page = add the file; its subdomain works instantly.
 *
 * SAFETY: the main site and all business-critical hosts are passed straight through, untouched —
 * this Worker only ever serves LP subdomains. The bank page cannot be affected.
 */
const LP_ORIGIN = "https://veyronpeptides.github.io/veyron-lp";

// Hosts the Worker must NEVER intercept — they serve the real business. Pass through as-is.
const PASSTHROUGH = new Set([
  "veyronbiologics.com",
  "www.veyronbiologics.com",
  "pay.veyronbiologics.com",
  "checkout.veyronbiologics.com",
]);

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    // Never touch the main site / payment / checkout — let Cloudflare serve them normally.
    if (PASSTHROUGH.has(host) || !host.endsWith(".veyronbiologics.com")) {
      return fetch(request);
    }

    const sub = host.slice(0, host.indexOf(".")); // e.g. "reta" from reta.veyronbiologics.com
    // Only the root path renders the LP; deeper paths (assets) fall through to the origin file.
    const path = url.pathname === "/" ? `/${sub}.html` : url.pathname;

    const res = await fetch(`${LP_ORIGIN}${path}`, { cf: { cacheTtl: 300 } });

    // If this subdomain has no page yet, send them to the catalog (attributed to the subdomain).
    if (res.status === 404) {
      return Response.redirect(`https://veyronbiologics.com/catalog?tr=${sub}`, 302);
    }
    // Serve the page; strip GitHub's headers, set a short cache.
    const out = new Response(res.body, res);
    out.headers.set("Cache-Control", "public, max-age=300");
    out.headers.delete("x-github-request-id");
    return out;
  },
};
