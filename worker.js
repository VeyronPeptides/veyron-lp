/**
 * Veyron landing-page router (Cloudflare Worker).
 * Every *.veyronbiologics.com subdomain → its matching landing page in the veyron-lp repo
 * (served from GitHub Pages). Adding a page = add the file; its subdomain works instantly.
 *
 * SAFETY: the main site and all business-critical hosts are passed straight through, untouched —
 * this Worker only ever serves LP subdomains. The bank page cannot be affected.
 *
 * Beyond routing, the Worker makes each LP a real ad-traffic entry point:
 *   1. Injects the Meta pixel bootstrap + a same-origin /px.js loader → PageView fires the RIGHT
 *      runner pixel on the landing page itself (previously LPs fired nothing).
 *   2. Proxies /px.js same-origin so it isn't blocked cross-subdomain (CORP) and resolves the runner.
 *   3. Carries the incoming ?tr=<runner> into every store link + sets a domain-wide cookie, so the
 *      runner key survives the LP → veyronbiologics.com hop and the sale attributes correctly.
 */
const LP_ORIGIN = "https://veyronpeptides.github.io/veyron-lp";
const MAIN = "https://veyronbiologics.com";

// Hosts the Worker must NEVER intercept — they serve the real business. Pass through as-is.
const PASSTHROUGH = new Set([
  "veyronbiologics.com",
  "www.veyronbiologics.com",
  "pay.veyronbiologics.com",
  "checkout.veyronbiologics.com",
]);

const cleanTr = (s) => (s || "").toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 48);

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();

    // Never touch the main site / payment / checkout — let Cloudflare serve them normally.
    if (PASSTHROUGH.has(host) || !host.endsWith(".veyronbiologics.com")) {
      return fetch(request);
    }

    const sub = host.slice(0, host.indexOf(".")); // e.g. "reta" from reta.veyronbiologics.com
    // Runner key: an explicit ?tr= from the ad (trParam) is the runner. If none, the page's own
    // subdomain is the key. When a runner IS present we FORCE their key onto every store link, replacing
    // the page's hardcoded default — otherwise the runner's attribution is lost at the click.
    const trParam = cleanTr(url.searchParams.get("tr"));
    const trKey = trParam || sub;

    // Same-origin pixel loader. reta.veyronbiologics.com/px.js → main /px.js?tr=<key>. Served from this
    // subdomain so the browser never trips CORP, and ?tr= resolves the runner's pixel server-side.
    if (url.pathname === "/px.js") {
      const px = await fetch(`${MAIN}/px.js?tr=${encodeURIComponent(trKey)}`, { cf: { cacheTtl: 300, cacheEverything: true } });
      const r = new Response(px.body, px);
      r.headers.set("Content-Type", "application/javascript; charset=utf-8");
      r.headers.set("Cache-Control", "public, max-age=300");
      r.headers.delete("etag");
      return r;
    }

    const path = url.pathname === "/" ? `/${sub}.html` : url.pathname;
    // Edge-cache the origin fetch (fast); per-request personalization happens in the transform below.
    const res = await fetch(`${LP_ORIGIN}${path}`, { cf: { cacheTtl: 600, cacheEverything: true } });

    // If this subdomain has no page yet, send them to the catalog (attributed to the runner key).
    if (res.status === 404) {
      return Response.redirect(`${MAIN}/catalog?tr=${encodeURIComponent(trKey)}`, 302);
    }

    const ct = res.headers.get("content-type") || "";
    if (!ct.includes("text/html")) {
      // Assets (images/css/js) pass through with the origin's cache headers — fast, unchanged.
      const a = new Response(res.body, res);
      a.headers.delete("x-github-request-id");
      return a;
    }

    // Fire the Meta pixel base + load the runner's pixel same-origin, and add ?tr= to every store link.
    const bootstrap =
      `<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?` +
      `n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;` +
      `n.loaded=!0;n.version='2.0';n.queue=[]}(window,document);</script>` +
      `<script src="/px.js?tr=${encodeURIComponent(trKey)}" async></script>`;

    const rewriter = new HTMLRewriter()
      .on("head", { element(el) { el.append(bootstrap, { html: true }); } })
      .on("a[href]", {
        element(el) {
          const href = el.getAttribute("href") || "";
          if (!/veyronbiologics\.com/i.test(href)) return;
          if (trParam) {
            // Explicit runner → force their key onto every store link (replace any hardcoded tr=).
            let h = /[?&]tr=/i.test(href) ? href.replace(/([?&])tr=[^&]*/i, `$1tr=${trParam}`) : `${href}${href.includes("?") ? "&" : "?"}tr=${trParam}`;
            el.setAttribute("href", h);
          } else if (!/[?&]tr=/.test(href)) {
            // No explicit runner + link untagged → tag with the page's own key.
            el.setAttribute("href", `${href}${href.includes("?") ? "&" : "?"}tr=${encodeURIComponent(trKey)}`);
          }
        },
      });

    const out = new Response(rewriter.transform(res).body, res);
    // Personalized by runner key → don't let a shared cache serve one runner's HTML to another.
    out.headers.set("Cache-Control", "private, no-store");
    // Persist the runner key across the LP → store hop, all subdomains, 90 days.
    out.headers.append("Set-Cookie", `veyron_tr=${trKey}; Domain=.veyronbiologics.com; Path=/; Max-Age=7776000; SameSite=Lax; Secure`);
    out.headers.delete("x-github-request-id");
    out.headers.delete("etag");
    return out;
  },
};
