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

// L3 A/B experiments — one entry per compound pair (PostHog experiments #381888–#381893, drafts).
// Flip a pair's `live` to true + deploy ONLY once (a) compliance greenlights that page for paid traffic
// AND (b) its PostHog experiment is LAUNCHED. While false: zero effect on that subdomain.
// DISABLED 2026-07-09 (Cam): the client redirect to the -2 variant caused a visible double-load/flash on
// the money pages (klow/nad/wolverine/bpc were bouncing to their -2). All paused → each page serves its
// own content, no reload. Re-enable a pair ONLY with a non-reload (server-side/same-URL) A/B mechanism.
const AB_PAIRS = {
  reta:      { live: false, flag: "reta-lp",      dest: "reta-2" },
  klow:      { live: false, flag: "klow-lp",      dest: "klow-2" },
  nad:       { live: false, flag: "nad-lp",       dest: "nad-2" },
  wolverine: { live: false, flag: "wolverine-lp", dest: "wolverine-2" },
  ghk:       { live: false, flag: "ghk-lp",       dest: "ghk-2" },
  bpc:       { live: false, flag: "bpc-lp",       dest: "bpc-2" },
};

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
      `<script src="/px.js?tr=${encodeURIComponent(trKey)}" async></script>` +
      // Microsoft Clarity — heatmaps + session recordings on the LPs (house-wide; dashboard access controlled in Clarity).
      `<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,"clarity","script","xiwmt0kmh3")</script>` +
      // PostHog — product analytics + feature flags + cohorts on the LPs (same project as the store).
      `<script>!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture identify alias people.set register register_once unregister onFeatureFlags getFeatureFlag getFeatureFlagPayload getFeatureFlagResult reloadFeatureFlags group".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);posthog.init('phc_wiushYFJjVJj6kJDeuMxGoMjTWgLVPmTMHx43s79Eyct',{api_host:'https://us.i.posthog.com',defaults:'2026-05-30',enable_heatmaps:true,persistence:'localStorage+cookie',cross_subdomain_cookie:true});</script>` +
      // Capture layer — scroll-depth milestones → PostHog, and an exit-intent (or deep-scroll on mobile)
      // FIRST25 email mini-form → POSTs to the store /api/lp-lead (GHL nurture) with veyron_tr attached +
      // fires Meta Lead. One snippet, every LP, no HTML regen. (No apostrophes/backticks/${ } inline.)
      `<script>(function(){var tr=(document.cookie.match(/veyron_tr=([a-z0-9_-]+)/i)||[])[1]||"";var f={},M=[25,50,75,90],tk=0,shown=0;function ck(){tk=0;var s=document.documentElement.scrollHeight-innerHeight;if(s<=0)return;var p=Math.min(100,Math.round(scrollY/s*100));M.forEach(function(m){if(p>=m&&!f[m]){f[m]=1;try{window.posthog&&posthog.capture("scroll_depth",{pct:m,path:location.pathname,lp:location.hostname})}catch(e){}if(m>=90)ei()}})}addEventListener("scroll",function(){if(!tk){tk=1;requestAnimationFrame(ck)}},{passive:1});function ei(){if(shown||sessionStorage.getItem("vx_ei"))return;shown=1;sessionStorage.setItem("vx_ei","1");try{window.posthog&&posthog.capture("exit_intent",{lp:location.hostname})}catch(e){}var w=document.createElement("div");w.style.cssText="position:fixed;inset:0;z-index:99999;background:rgba(10,8,6,.7);display:flex;align-items:center;justify-content:center;padding:20px";w.innerHTML="<div style=\\"background:#fffdf8;max-width:400px;border-radius:16px;padding:28px;text-align:center;font-family:system-ui,sans-serif;position:relative\\"><button id=vxX style=\\"position:absolute;top:8px;right:14px;border:0;background:0;font-size:22px;cursor:pointer;color:#aaa\\">&times;</button><div style=\\"font:700 11px/1 monospace;letter-spacing:2px;text-transform:uppercase;color:#b8912f\\">Before you go</div><h3 style=\\"font-family:Georgia,serif;font-size:24px;margin:8px 0 6px;color:#161310\\">25% off your first order</h3><p style=\\"color:#5c5647;font-size:14px;margin:0 0 16px\\">Drop your email and we will send code <b>FIRST25</b>.</p><form id=vxF><input id=vxE type=email required placeholder=you@email.com style=\\"width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;font-size:15px;margin-bottom:10px\\"><button type=submit style=\\"width:100%;padding:13px;border:0;border-radius:8px;background:#b8912f;color:#12100c;font-weight:800;text-transform:uppercase;letter-spacing:.5px;font-size:13px;cursor:pointer\\">Send me the code</button></form><div id=vxOk style=\\"display:none;color:#3a7a3a;font-size:14px;margin-top:8px\\">Check your inbox for FIRST25 - see you at checkout!</div></div>";document.body.appendChild(w);function close(){w.remove()}w.addEventListener("click",function(e){if(e.target===w)close()});document.getElementById("vxX").onclick=close;document.getElementById("vxF").onsubmit=function(e){e.preventDefault();var em=document.getElementById("vxE").value;try{window.posthog&&posthog.capture("lp_lead",{lp:location.hostname})}catch(x){}try{window.fbq&&fbq("track","Lead")}catch(x){}fetch("https://veyronbiologics.com/api/lp-lead",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({email:em,tr:tr,url:location.href})}).catch(function(){});document.getElementById("vxF").style.display="none";document.getElementById("vxOk").style.display="block";setTimeout(close,2600)}}addEventListener("mouseout",function(e){if(e.clientY<=0&&!e.relatedTarget)ei()})})()</script>` +
      // L3 A/B split — STAGED per pair via AB_PAIRS above. While a pair is live: its entry page hides
      // ≤300ms for EVERYONE (equal delay, no bias); the 'test' group goes to the -2 variant with ?tr=
      // preserved; the flag exposure ties to the store purchase via the cross-subdomain PostHog person.
      (AB_PAIRS[sub] && AB_PAIRS[sub].live
        ? `<script>(function(){var e=document.documentElement,v0=e.style.visibility;e.style.visibility='hidden';var d=0;function show(){if(!d){d=1;e.style.visibility=v0||''}}setTimeout(show,300);function run(){try{if(posthog.getFeatureFlag('${AB_PAIRS[sub].flag}')==='test'){location.replace('https://${AB_PAIRS[sub].dest}.veyronbiologics.com/'+(location.search||''));return}}catch(x){}show()}if(window.posthog&&posthog.onFeatureFlags){posthog.onFeatureFlags(run)}else{setTimeout(run,250)}})()</script>`
        : "");

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
