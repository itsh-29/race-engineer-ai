const compoundClass = (compound) => {
  if (compound === "SOFT") return "compound-soft"
  if (compound === "MEDIUM") return "compound-medium"
  return "compound-hard"
}

const compoundDot = (compound) => {
  if (compound === "SOFT") return "soft"
  if (compound === "MEDIUM") return "medium"
  return "hard"
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(1)
  return `${mins}m ${secs}s`
}

export default function StrategyResults({ strategies, selected, onSelect }) {
  return (
    <div className="card">
      <p className="card-title">Strategy Rankings</p>
      <div className="strategy-list">
        {strategies.map((s) => (
          <div
            key={s.rank}
            className={`strategy-card ${selected?.rank === s.rank ? "active" : ""} ${s.rank === 1 ? "optimal" : ""}`}
            onClick={() => onSelect(s)}
          >
            {s.rank === 1 && <div className="optimal-badge">Optimal</div>}

            <div className="strategy-rank">#{s.rank}</div>

            <div className="strategy-stints">
              {s.stints.map((stint, i) => (
                <span key={i} style={{ display: "flex", alignItems: "center" }}>
                  <span className={`compound-dot ${compoundDot(stint.compound)}`}></span>
                  <span className={compoundClass(stint.compound)}>
                    {stint.compound}
                  </span>
                  <span style={{ color: "#444", fontSize: "11px", marginLeft: "3px" }}>
                    ({stint.laps}L)
                  </span>
                  {i < s.stints.length - 1 && (
                    <span className="strategy-arrow"> → </span>
                  )}
                </span>
              ))}
            </div>

            <div className="strategy-time">
              <span>Pit Lap {s.pit_laps.join(", ")}</span>
              <strong>{formatTime(s.total_time)}</strong>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}