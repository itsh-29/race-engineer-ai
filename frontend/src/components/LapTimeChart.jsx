import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Area, AreaChart } from "recharts"

const COMPOUND_COLORS = {
  SOFT: "#ff4444",
  MEDIUM: "#ffaa00",
  HARD: "#cccccc"
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const compound = payload[0]?.payload?.compound
    return (
      <div style={{
        background: "#1a1a1a",
        border: "1px solid #333",
        borderRadius: "10px",
        padding: "10px 14px",
        fontSize: "12px"
      }}>
        <div style={{ color: "#666", marginBottom: "4px" }}>Lap {label}</div>
        <div style={{ color: COMPOUND_COLORS[compound] || "#fff", fontWeight: 700 }}>
          {compound}
        </div>
        <div style={{ color: "#fff", fontSize: "14px", fontWeight: 700 }}>
          {payload[0]?.value?.toFixed(3)}s
        </div>
      </div>
    )
  }
  return null
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
      <p style={{ color: "var(--text-muted)", fontSize: "13px", paddingTop: "8px" }}>
        Select a strategy to see lap time simulation
      </p>
    </div>
  )

  const pitLaps = []
  for (let i = 1; i < lapTimes.length; i++) {
    if (lapTimes[i].compound !== lapTimes[i - 1].compound) {
      pitLaps.push(lapTimes[i].lap)
    }
  }

  return (
    <div className="card">
      <p className="card-title">Race Pace Simulation</p>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={lapTimes} margin={{ top: 10, right: 10, bottom: 20, left: 10 }}>
          <defs>
            <linearGradient id="lapGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#e8002d" stopOpacity={0.15} />
              <stop offset="95%" stopColor="#e8002d" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="lap"
            stroke="#333"
            tick={{ fill: "#555", fontSize: 11 }}
            label={{ value: "Lap", position: "insideBottom", offset: -10, fill: "#555", fontSize: 11 }}
          />
          <YAxis
            stroke="#333"
            tick={{ fill: "#555", fontSize: 11 }}
            domain={["auto", "auto"]}
            tickFormatter={(v) => `${v.toFixed(0)}s`}
            width={45}
          />
          <Tooltip content={<CustomTooltip />} />
          {pitLaps.map(lap => (
            <ReferenceLine
              key={lap}
              x={lap}
              stroke="#e8002d"
              strokeDasharray="3 3"
              strokeOpacity={0.6}
              label={{ value: "PIT", position: "insideTopRight", fill: "#e8002d", fontSize: 9, fontWeight: 700 }}
            />
          ))}
          <Area
            type="monotone"
            dataKey="time"
            stroke="#e8002d"
            strokeWidth={2}
            fill="url(#lapGradient)"
            dot={(props) => {
              const { cx, cy, payload } = props
              return (
                <circle
                  key={`dot-${payload.lap}`}
                  cx={cx} cy={cy} r={2.5}
                  fill={COMPOUND_COLORS[payload.compound]}
                  stroke="none"
                />
              )
            }}
            isAnimationActive={true}
            animationDuration={800}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div style={{ display: "flex", gap: "20px", justifyContent: "center", marginTop: "8px" }}>
        {Object.entries(COMPOUND_COLORS).map(([compound, color]) => (
          <span key={compound} style={{
            fontSize: "10px",
            color,
            fontWeight: 700,
            letterSpacing: "0.1em",
            display: "flex",
            alignItems: "center",
            gap: "5px"
          }}>
            <span style={{
              width: "8px", height: "8px",
              borderRadius: "50%",
              background: color,
              display: "inline-block"
            }}></span>
            {compound}
          </span>
        ))}
      </div>
    </div>
  )
}