export interface Prediction {
  id: number;
  studentId: number;
  student?: string;
  predictedGrade: number;
  confidence: number;
  riskLevel: 'low' | 'medium' | 'high';
  factors: string[];
  generatedAt: Date;
  semester: string;
}