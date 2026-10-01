import { useState, useEffect } from 'react'

function App() {
  const [recommendations, setRecommendations] = useState([])
  const [quality, setQuality] = useState([])

  useEffect(() => {
    // Fetch Recommendations
    fetch('http://localhost:8000/recommendations')
      .then(res => res.json())
      .then(data => setRecommendations(data))
      .catch(err => console.error("Failed to fetch recommendations", err))

    // Fetch Data Quality Warnings
    fetch('http://localhost:8000/data-quality')
      .then(res => res.json())
      .then(data => setQuality(data))
      .catch(err => console.error("Failed to fetch data quality", err))
  }, [])

  return (
    <div className="p-8 font-sans max-w-6xl mx-auto text-slate-800">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-bold">Business Decision Engine</h1>
        <p className="text-slate-500 mt-2">Actionable insights generated from historical transaction data.</p>
      </header>

      {quality.length > 0 && (
        <section className="mb-8 p-4 bg-orange-50 border border-orange-200 rounded-lg">
          <h2 className="text-lg font-semibold text-orange-800 mb-2">Data Quality Warnings</h2>
          <ul className="list-disc pl-5 text-orange-700 text-sm">
            {quality.map((q, i) => (
              <li key={i}>Detected {q.count} instances of {q.type} in field <strong>{q.field}</strong>.</li>
            ))}
          </ul>
        </section>
      )}

      <section>
        <h2 className="text-2xl font-semibold mb-6">Opportunities & Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendations.length === 0 ? (
            <p className="text-slate-500">No current actionable recommendations based on recent data.</p>
          ) : (
            recommendations.map((rec, i) => (
              <div key={i} className={`p-6 rounded-lg shadow-sm border-t-4 bg-white ${rec.priority === 'HIGH' ? 'border-red-500' : 'border-blue-500'}`}>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className={`text-xs font-bold tracking-wider px-2 py-1 rounded ${rec.priority === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
                      {rec.priority} • {rec.type.replace('_', ' ')}
                    </span>
                    <h3 className="text-xl font-bold mt-3">{rec.title}</h3>
                  </div>
                  <div className="text-right ml-4">
                    <span className="block text-2xl font-bold text-slate-700">
                      {rec.metric_value > 0 && rec.metric !== 'days_since_last_purchase' ? '+' : ''}
                      {rec.metric_value}
                      {rec.metric.includes('pct') ? '%' : ''}
                    </span>
                    <span className="text-xs text-slate-400 uppercase">{rec.metric}</span>
                  </div>
                </div>
                
                <p className="text-slate-600 font-medium mb-4">{rec.description}</p>
                
                <div className="text-sm text-slate-500 bg-slate-50 p-3 rounded border border-slate-100">
                  <strong className="text-slate-700">Evidence:</strong> {rec.evidence}
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  )
}

export default App
