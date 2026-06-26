import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts"

const COMPOUND_COLORS = {
  SOFT: "#ff4444",
  MEDIUM: "#ffaa00",
  HARD: "#cccccc"
}

export default function LapTimeChart({ lapTimes, loading }) {
  if (loading) return (
    <div className="card">
      <p className="card-title">Race Pace</p>
      <div className="loading">
        <div className="spinner"></div>
        Simulating lap times...
      </div>
    </div>
  )

  if (!lapTimes.length) return (
    <div className="card">
      <p className="card-title">Race Pace</p>
      <p style={{ color: "var(--text-muted)", fontSize: "14px" }}>
        Select a strategy to see lap time simulation
      </p>
    </div>
  )

  // Find pit laps (where compound changes)
  const pitLaps = []
  for (let i = 1; i < lapTimes.length; i++) {
    if (lapTimes[i].compound !== lapTimes[i - 1].compound) {
      pitLaps.push(lapTimes[i].lap)
    }
  }

  return (
    <div className="card">
      <p className="card-title">Race Pace Simulation</p>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={lapTimes} margin={{ top: 5, right: 10, bottom: 5, left: 10 }}>
          <XAxis
            dataKey="lap"
            stroke="#444"
            tick={{ fill: "#888", fontSize: 11 }}
            label={{ value: "Lap", position: "insideBottom", fill: "#888", fontSize: 11 }}
          />
          <YAxis
            stroke="#444"
            tick={{ fill: "#888", fontSize: 11 }}
            domain={["auto", "auto"]}
            tickFormatter={(v) => `${v.toFixed(1)}s`}
          />
          <Tooltip
            contentStyle={{ background: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "8px" }}
            labelStyle={{ color: "#888", fontSize: "12px" }}
            formatter={(value, name, props) => [
              `${value.toFixed(3)}s`,
              props.payload.compound
            ]}
          />
          {pitLaps.map(lap => (
            <ReferenceLine
              key={lap}
              x={lap}
              stroke="#e8002d"
              strokeDasharray="4 4"
              label={{ value: "PIT", position: "top", fill: "#e8002d", fontSize: 10 }}
            />
          ))}
          <Line
            type="monotone"
            dataKey="time"
            stroke="#e8002d"
            dot={(props) => {
              const { cx, cy, payload } = props
              return (
                <circle
                  key={`dot-${payload.lap}`}
                  cx={cx} cy={cy} r={2}
                  fill={COMPOUND_COLORS[payload.compound]}
                  stroke="none"
                />
              )
            }}
            strokeWidth={2}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>

      <div style={{ display: "flex", gap: "16px", marginTop: "12px", justifyContent: "center" }}>
        {Object.entries(COMPOUND_COLORS).map(([compound, color]) => (
          <span key={compound} style={{ fontSize: "11px", color, fontWeight: 700 }}>
            ● {compound}
          </span>
        ))}
      </div>
    </div>
  )
}