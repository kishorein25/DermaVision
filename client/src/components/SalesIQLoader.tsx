import { useEffect } from "react";

export function SalesIQLoader() {
  useEffect(() => {
    // Avoid adding script twice
    const existing = document.getElementById("zsiqscript");
    if (existing) return;

    // @ts-ignore
    window.$zoho = window.$zoho || {};
    // @ts-ignore
    window.$zoho.salesiq = window.$zoho.salesiq || {
      ready: function () {},
    };

    const d = document;
    const s = d.createElement("script");
    s.type = "text/javascript";
    s.id = "zsiqscript";
    s.defer = true;
    s.src =
      "https://salesiq.zohopublic.com/widget?wc=siqfdade8f99cecdec53ba1ccf63235c1b20b90b97f984bc983685b13b48d165b7e";

    const t = d.getElementsByTagName("script")[0];
    if (t && t.parentNode) {
      t.parentNode.insertBefore(s, t);
    } else {
      d.body.appendChild(s);
    }
  }, []);

  return null;
}
