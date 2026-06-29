import axios from "axios";

const api = axios.create({
  baseURL: "https://race-engineer-ai-api.onrender.com",
})


export const pollStatus =(jobID) =>api.get(`/status/${jobID}`);
export const getResults =(jobID) =>api.get(`/results/${jobID}`);
export const optimizeStrategy=(data)=> api.post("/optimize",data);
export const simulateStint= (data)=> api.post("/simulate",data);
export const compareCompounds=(data)=> api.post("/compare",data);
export const explainStrategy=(data)=> api.post("/explain",data);
export const chatWithEngineer=(data)=> api.post("/chat",data);
