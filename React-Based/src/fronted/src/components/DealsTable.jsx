import React, { useEffect, useState } from "react";

// Props:
// - deals: array of { opportunity_id, sales_agent, product, account, engage_date, close_date, close_value }
// - apiBase: optional base URL for the prediction API (defaults to '')

export default function DealsTable({ deals = [], apiBase = "" }) {
  const [predictions, setPredictions] = useState({}); // map dealId -> { win_prob }
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!deals || deals.length === 0) return;
    // Batch predict: call /predict_deal for each deal (or implement a batch endpoint server-side)
    let mounted = true;
    const fetchPredictions = async () => {
      setLoading(true);
      const newPreds = {};
      try {
        await Promise.all(
          deals.map(async (d) => {
            const payload = {
              opportunity_id: d.opportunity_id,
              sales_agent: d.sales_agent,
              product: d.product,
              account: d.account,
              engage_date: d.engage_date,
              close_date: d.close_date,
              close_value: d.close_value,
            };

            const res = await fetch(`${apiBase}/predict_deal`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload),
            });

            if (res.ok) {
              const json = await res.json();
              newPreds[d.opportunity_id] = json;
            } else {
              newPreds[d.opportunity_id] = { error: `status ${res.status}` };
            }
          })
        );

        if (mounted) setPredictions(newPreds);
      } catch (err) {
        console.error("Error fetching predictions", err);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchPredictions();
    return () => (mounted = false);
  }, [deals, apiBase]);

  // choose color for risk bar: low win_prob -> red (high risk), high win_prob -> green (low risk)
  const riskColor = (p) => {
    // p in [0,1]
    const clamped = Math.max(0, Math.min(1, p));
    // interpolate from red -> yellow -> green
    const r = Math.round(
      255 * (1 - Math.min(1, clamped * 2)) +
        255 * (clamped > 0.5 ? 1 - (clamped - 0.5) * 2 : 0)
    );
    const g = Math.round(255 * Math.min(1, clamped * 2));
    return `rgb(${r}, ${g}, 60)`; // keep a warm tint
  };

  return (
    <div className="w-full">
      <div className="overflow-x-auto bg-white rounded-lg shadow p-4">
        <table className="w-full table-auto">
          <thead>
            <tr className="text-left text-sm text-gray-600">
              <th className="px-3 py-2">Opportunity ID</th>
              <th className="px-3 py-2">Agent</th>
              <th className="px-3 py-2">Product</th>
              <th className="px-3 py-2">Account</th>
              <th className="px-3 py-2">Close Value</th>
              <th className="px-3 py-2">Win Prob</th>
              <th className="px-3 py-2">Risk Bar</th>
            </tr>
          </thead>
          <tbody>
            {deals.map((d) => {
              const pred = predictions[d.opportunity_id];
              const winProb =
                pred && pred.win_probability != null
                  ? Number(pred.win_probability)
                  : null;
              return (
                <tr key={d.opportunity_id} className="border-t">
                  <td className="px-3 py-2 text-sm">{d.opportunity_id}</td>
                  <td className="px-3 py-2 text-sm">{d.sales_agent}</td>
                  <td className="px-3 py-2 text-sm">{d.product}</td>
                  <td className="px-3 py-2 text-sm">{d.account}</td>
                  <td className="px-3 py-2 text-sm">£{d.close_value}</td>
                  <td className="px-3 py-2 text-sm">
                    {winProb == null ? (
                      <span className="text-gray-400">—</span>
                    ) : (
                      <span className="font-medium">
                        {Math.round(winProb * 100)}%
                      </span>
                    )}
                  </td>
                  <td className="px-3 py-2 w-48">
                    <div className="h-4 bg-gray-100 rounded overflow-hidden">
                      <div
                        className="h-full"
                        style={{
                          width:
                            winProb != null
                              ? `${Math.round(winProb * 100)}%`
                              : "0%",
                          background:
                            winProb != null
                              ? riskColor(1 - winProb)
                              : "transparent",
                          transition: "width 300ms ease",
                        }}
                        title={
                          winProb != null
                            ? `Win ${Math.round(winProb * 100)}%`
                            : "No prediction"
                        }
                      />
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {loading && (
          <div className="text-sm text-gray-500 mt-2">
            Fetching predictions...
          </div>
        )}
      </div>
    </div>
  );
}
