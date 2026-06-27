const TRACKS = ["Monaco","Silverstone","Monza","Spain","Hungary","Bahrain"]
const DRIVERS= ["VER","HAM","LEC","NOR","SAI","RUS","ALO","PIA"]

export default function StrategyForm({
    track,setTrack,
    driver,setDriver,
    raceLaps,setRaceLaps,
    pitPenalty,setPitPenalty,
    onOptimize,
    loading
}){
    return(
        <div className="card section">
            <p className="card-title">Race Configuration</p>
            <div className="form-grid">

                <div className="form-group">
                    <label>Track</label>
                    <select value={track} onChange={e=>setTrack(e.target.value)}>
                        {TRACKS.map(t=> <option key={t}>{t}</option>)}
                    </select>
                </div>

                <div className="form-group">
                    <label>Driver</label>
                    <select value={driver} onChange={e=>setDriver(e.target.value)}>
                        {DRIVERS.map(t=> <option key={t}>{t}</option>)}
                    </select>
                </div>

                <div className="form-group">
                    <label>Race Laps</label>
                    <input
                        type="number"
                        value={raceLaps}
                        onChange={e=>setRaceLaps(Number(e.target.value))}
                        min={20} max={80}
                    />
                </div>

                <div className="form-group">
                    <label>Pit Stop Penalty(s)</label>
                    <input
                        type="number"
                        value={pitPenalty}
                        onChange={e=>setPitPenalty(Number(e.target.value))}
                        min={15} max={35}
                    />
                </div>
            </div>
            <button 
                className="btn-primary"
                onClick={onOptimize}
                disabled={loading}
            >
                {loading ? "Optimizing...":"Optimize Strategy"}
            </button>
        </div>
    )
}