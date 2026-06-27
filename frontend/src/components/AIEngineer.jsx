import { useState } from "react"

export default function AIEngineer({ explanation, loadingAI, chatMessages, onChat }) {
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim()) return
    onChat(input.trim())
    setInput("")
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend()
  }

  return (
    <div className="card section">
      <div className="ai-header">
        <div className="ai-avatar">🏎️</div>
        <div>
          <div className="ai-title">AI Race Engineer</div>
          <div className="ai-subtitle">Powered by Gemini 2.5 Flash</div>
        </div>
      </div>

      {loadingAI ? (
        <div className="loading">
          <div className="spinner"></div>
          Analysing strategy and preparing briefing...
        </div>
      ) : (
        explanation && (
          <p className="ai-explanation">{explanation}</p>
        )
      )}

      {chatMessages.length > 0 && (
        <div className="chat-messages">
          {chatMessages.map((msg, i) => (
            <div
              key={i}
              className={`chat-message ${msg.role === "user" ? "user" : "ai"}`}
            >
              {msg.text}
            </div>
          ))}
        </div>
      )}

      {explanation && (
        <>
          <div className="divider"></div>
          <div className="chat-input-row">
            <input
              type="text"
              placeholder="Ask your race engineer anything..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="btn-primary" onClick={handleSend}>
              Send
            </button>
          </div>
        </>
      )}
    </div>
  )
}