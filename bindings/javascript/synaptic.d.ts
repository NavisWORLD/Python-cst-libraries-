export function gaussianAffinity(a:number[],b:number[],sigma?:number):number;
export function affinityMatrix(states:number[][],sigma?:number):number[][];
export function gatedBlend(standard:number,affinity:number,gate:number):number;
export function stateStep(state:number[],signal:number[],options?:{decay?:number;gain?:number;dt?:number}):number[];
export class SynapticFunction{constructor(options?:{sigma?:number;gate?:number});sigma:number;gate:number;affinity(a:number[],b:number[]):number;matrix(states:number[][]):number[][];blend(standard:number,affinity:number,gate?:number):number;step(state:number[],signal:number[],options?:{decay?:number;gain?:number;dt?:number}):number[];}
