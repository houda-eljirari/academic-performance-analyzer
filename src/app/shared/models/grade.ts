export interface Grade {
  id: number;
  studentId: number;
  subject: string;
  score: number;
  maxScore: number;
  semester: string;
  academicYear: string;
  date: Date;
  type: 'exam' | 'quiz' | 'assignment' | 'project';
}