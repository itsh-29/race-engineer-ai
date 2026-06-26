import axios from "axios";

const api = axios.create({
    baseURL:"http://127.0.0.1:8000",
})

export const optimizeStrategy=(data)=> api.post("/optimize",data);
export const stimulateStint= (data)=> api.post("/simulate",data);
export const compareCompounds=(data)=> api.post("/compare",data);
export const explainStrategy=(data)=> api.post("/explain",data);
export const chatWithEngineer=(data)=> api.post("/chat",data);
