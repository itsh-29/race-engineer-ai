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
      <p className="card-title">AI Race Engineer</p>

      {loadingAI ? (
        <div className="loading">
          <div className="spinner"></div>
          Briefing in progress...
        </div>
      ) : (
        explanation && (
          <p className="ai-explanation">{explanation}</p>
        )
      )}

      {chatMessages.length > 0 && (
        <div className="chat-messages">
          {chatMessages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.role === "user" ? "user" : "ai"}`}>
              {msg.text}
            </div>
          ))}
        </div>
      )}

      {explanation && (
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
      )}
    </div>
  )
}