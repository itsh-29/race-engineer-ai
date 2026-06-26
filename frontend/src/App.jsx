import { useState } from "react"
import "./App.css"
import { optimizeStrategy, simulateStint, explainStrategy, chatWithEngineer } from "./api/client"

import Header from "./components/Header"
import StrategyForm from "./components/StrategyForm"
import StrategyResults from "./components/StrategyResults"
import LapTimeChart from "./components/LapTimeChart"
import AIEngineer from "./components/AIEngineer"

export default function App() {
  // Form state
  const [track, setTrack] = useState("Monaco")
  const [driver, setDriver] = useState("VER")
  const [raceLaps, setRaceLaps] = useState(78)
  const [pitPenalty, setPitPenalty] = useState(25)

  // Result state
  const [strategies, setStrategies] = useState([])
  const [selectedStrategy, setSelectedStrategy] = useState(null)
  const [lapTimes, setLapTimes] = useState([])
  const [explanation, setExplanation] = useState("")
  const [chatMessages, setChatMessages] = useState([])

  // Loading state
  const [loadingOptimize, setLoadingOptimize] = useState(false)
  const [loadingChart, setLoadingChart] = useState(false)
  const [loadingAI, setLoadingAI] = useState(false)

  // ── Step 1: Optimize ──
  const handleOptimize = async () => {
    setLoadingOptimize(true)
    setStrategies([])
    setSelectedStrategy(null)
    setLapTimes([])
    setExplanation("")
    setChatMessages([])

    try {
      const res = await optimizeStrategy({
        track, driver,
        race_laps: raceLaps,
        pit_stop_penalty: pitPenalty
      })
      setStrategies(res.data.strategies)
      handleSelectStrategy(res.data.strategies[0], res.data.strategies)
    } catch (e) {
      console.error(e)
    } finally {
      setLoadingOptimize(false)
    }
  }

  // ── Step 2: Select a strategy → load chart + AI ──
  const handleSelectStrategy = async (strategy, allStrategies) => {
    setSelectedStrategy(strategy)
    setLoadingChart(true)
    setLoadingAI(true)

    const strats = allStrategies || strategies

    // Build full race lap times across all stints
    try {
      let allLaps = []
      let lapCursor = 1
      for (const stint of strategy.stints) {
        const res = await simulateStint({
          track, driver,
          compound: stint.compound,
          stint_length: stint.laps,
          start_lap: lapCursor
        })
        allLaps = [...allLaps, ...res.data.laps.map((time, i) => ({
          lap: lapCursor + i,
          time: parseFloat(time.toFixed(3)),
          compound: stint.compound
        }))]
        lapCursor += stint.laps
      }
      setLapTimes(allLaps)
    } catch (e) {
      console.error(e)
    } finally {
      setLoadingChart(false)
    }

    // Get AI explanation
    try {
      const res = await explainStrategy({ track, driver, strategies: strats })
      setExplanation(res.data.explanation)
    } catch (e) {
      console.error(e)
    } finally {
      setLoadingAI(false)
    }
  }

  // ── Step 3: Chat ──
  const handleChat = async (message) => {
    setChatMessages(prev => [...prev, { role: "user", text: message }])
    try {
      const res = await chatWithEngineer({ track, driver, strategies, message })
      setChatMessages(prev => [...prev, { role: "ai", text: res.data.response }])
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="app">
      <Header />

      <StrategyForm
        track={track} setTrack={setTrack}
        driver={driver} setDriver={setDriver}
        raceLaps={raceLaps} setRaceLaps={setRaceLaps}
        pitPenalty={pitPenalty} setPitPenalty={setPitPenalty}
        onOptimize={handleOptimize}
        loading={loadingOptimize}
      />

      {strategies.length > 0 && (
        <>
          <div className="charts-grid section">
            <StrategyResults
              strategies={strategies}
              selected={selectedStrategy}
              onSelect={(s) => handleSelectStrategy(s)}
            />
            <LapTimeChart
              lapTimes={lapTimes}
              loading={loadingChart}
            />
          </div>

          <AIEngineer
            explanation={explanation}
            loadingAI={loadingAI}
            chatMessages={chatMessages}
            onChat={handleChat}
          />
        </>
      )}
    </div>
  )
}