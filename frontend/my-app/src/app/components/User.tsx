import { useState } from "react";
import { AxiosError } from "axios";
import api from "@/src/app/api/users/api";
import { signOut, useSession } from "next-auth/react";

interface EvaluationResult {
  final_score: string | number;
  match_level: string;
  missing_skills: string[];
  suggestions: string[];
}

const jdDataset = [
  {
    role: "Software Engineer",
    jd: "We are seeking a Software Engineer to design, develop, and maintain scalable software systems. The role requires strong knowledge of data structures, algorithms, object-oriented programming, and problem solving. Experience with Python or Java, version control using Git, REST API development, and database systems is expected."
  },
  {
    role: "Backend Developer",
    jd: "The Backend Developer will build and maintain server-side applications and RESTful APIs. Required skills include Python, FastAPI, SQL databases, authentication mechanisms, API validation, and performance optimization. Familiarity with deployment workflows and backend debugging is important."
  },
  {
    role: "Frontend Developer",
    jd: "We are looking for a Frontend Developer to create responsive and user-friendly web interfaces. The candidate should have experience with HTML, CSS, JavaScript, and modern frameworks such as React or Next.js. Knowledge of API integration, state management, and UI optimization is required."
  },
  {
    role: "Full Stack Developer",
    jd: "The Full Stack Developer will work across both frontend and backend systems. Required skills include JavaScript, React or Next.js for frontend development, FastAPI or Node.js for backend services, REST API design, database integration, and full-stack debugging."
  },
  {
    role: "Data Analyst",
    jd: "The Data Analyst will analyze structured data to extract insights and support decision making. Required skills include SQL, Python, data cleaning, exploratory data analysis, data visualization, and basic statistical techniques. Experience with dashboards and reporting is preferred."
  },
  {
    role: "Machine Learning Engineer",
    jd: "We are hiring a Machine Learning Engineer to build and deploy predictive models. The candidate should be proficient in Python, machine learning algorithms, data preprocessing, feature engineering, and model evaluation. Experience with libraries such as scikit-learn, TensorFlow, or PyTorch is expected."
  },
  {
    role: "AI / NLP Engineer",
    jd: "The AI/NLP Engineer will develop natural language processing pipelines for text analysis. Required skills include Python, spaCy or NLTK, regex-based text processing, entity extraction, semantic analysis, and deploying NLP systems in production environments."
  },
  {
    role: "DevOps Engineer",
    jd: "The DevOps Engineer will manage application deployment and infrastructure. Required skills include Linux, Docker, CI/CD pipelines, cloud platforms, automation scripting, and monitoring systems. Experience with system reliability and deployment workflows is essential."
  },
  {
    role: "Cyber Security Analyst",
    jd: "We are looking for a Cyber Security Analyst to identify and mitigate security risks. Required skills include network security, vulnerability assessment, threat analysis, secure coding practices, and familiarity with security tools and protocols."
  },
  {
    role: "QA / Software Testing Engineer",
    jd: "The QA Engineer will ensure software quality through manual and automated testing. Required skills include test case design, bug tracking, API testing, automation frameworks, and understanding of software development life cycles."
  }
];

export default function User() {
  const { data: session } = useSession();
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<EvaluationResult | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);

  const handleRoleSelect = (selectedJd: string) => {
    setJd(selectedJd);
    setShowDropdown(false);
  };

  const handleSubmit = async () => {
    if (!file || !jd) return alert("Upload resume and enter JD");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("jd_data", jd);
    if (session?.user?.email) {
      formData.append("email", session.user.email);
    }

    try {
      setLoading(true);
      setError(null);
      setResult(null);
      const res = await api.post("/evaluate", formData);
      setResult(res.data);
    } catch (error: unknown) {
      const err = error as AxiosError<{ detail: string }>;
      console.error(err);
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-indigo-900 via-purple-900 to-pink-900 py-12 px-4 sm:px-6 lg:px-8 font-sans text-gray-100 flex items-center justify-center">
      <main className="max-w-4xl w-full space-y-8 bg-white/10 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20">
        <div className="flex justify-end">
             <button onClick={() => signOut()} className="text-sm text-gray-300 hover:text-white pb-2">Sign Out</button>
        </div>
        <div className="text-center">
          <h1 className="text-5xl font-extrabold tracking-tight mb-2 bg-linear-to-r from-blue-200 to-pink-200 bg-clip-text text-transparent">
            ATS Resume Evaluator
          </h1>
          <p className="text-lg text-gray-300">
            Optimize your resume for Applicant Tracking Systems
          </p>
        </div>

        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* File Upload Section */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300 ml-1">
                Upload Resume (PDF)
              </label>
              <div className="relative group">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="block w-full text-sm text-gray-300
                    file:mr-4 file:py-3 file:px-6
                    file:rounded-full file:border-0
                    file:text-sm file:font-semibold
                    file:bg-indigo-600 file:text-white
                    hover:file:bg-indigo-500
                    cursor-pointer
                    bg-white/5 rounded-xl border border-white/10
                    focus:outline-none focus:ring-2 focus:ring-indigo-500 box-border p-2"
                />
              </div>
            </div>

            {/* Submit Button Section */}
             <div className="flex items-end">
                <button
                  onClick={handleSubmit}
                  disabled={loading}
                  className={`w-full py-4 px-6 rounded-xl font-bold text-white shadow-lg transform transition-all duration-200 
                    ${
                      loading
                        ? "bg-gray-600 cursor-not-allowed opacity-70"
                        : "bg-linear-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 hover:scale-[1.02] hover:shadow-indigo-500/25 active:scale-[0.98]"
                    }`}
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Evaluating...
                    </span>
                  ) : (
                    "Evaluate Resume"
                  )}
                </button>
             </div>
          </div>

          {/* Job Description Section */}
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <label className="block text-sm font-medium text-gray-300 ml-1">
                Job Description
              </label>
              
              {/* Dropdown UI */}
              <div className="relative">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="flex items-center justify-between gap-2 px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-sm font-medium text-gray-200 hover:bg-white/20 transition-all focus:outline-none"
                >
                  Quick Select Role
                  <svg className={`w-4 h-4 transition-transform ${showDropdown ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                {showDropdown && (
                  <ul className="absolute right-0 mt-2 w-64 bg-slate-800 border border-white/10 rounded-xl shadow-2xl z-50 py-2 max-h-60 overflow-y-auto backdrop-blur-xl animate-in fade-in zoom-in-95 duration-100">
                    {jdDataset.map((item) => (
                      <li key={item.role}>
                        <button
                          onClick={() => handleRoleSelect(item.jd)}
                          className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-indigo-600 hover:text-white transition-colors"
                        >
                          {item.role}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>

            <textarea
              placeholder="Paste the Job Description here to compare against your resume..."
              value={jd}
              onChange={(e) => setJd(e.target.value)}
              className="w-full h-48 p-4 bg-white/5 border border-white/10 rounded-xl text-gray-200 placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:outline-none resize-none transition-all"
            />
          </div>
        </div>


        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/50 rounded-xl p-4 text-red-200 flex items-center gap-3 animate-in fade-in slide-in-from-top-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 mt-8 space-y-6">
            <div className="bg-white/5 border border-white/10 rounded-2xl p-6 md:p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                
                {/* Score and Match Level */}
                <div className="text-center space-y-4">
                  <div className="relative inline-flex items-center justify-center">
                    <svg className="w-32 h-32 transform -rotate-90">
                      <circle
                        className="text-gray-700"
                        strokeWidth="8"
                        stroke="currentColor"
                        fill="transparent"
                        r="58"
                        cx="64"
                        cy="64"
                      />
                      <circle
                        className="text-indigo-500 transition-all duration-1000 ease-out"
                        strokeWidth="8"
                        strokeDasharray={365}
                        strokeDashoffset={365 - (365 * Number(result.final_score)) / 100}
                        strokeLinecap="round"
                        stroke="currentColor"
                        fill="transparent"
                        r="58"
                        cx="64"
                        cy="64"
                      />
                    </svg>
                    <span className="absolute text-3xl font-bold text-white">
                      {result.final_score}%
                    </span>
                  </div>
                  <div>
                    <h3 className="text-gray-400 text-sm uppercase tracking-wider">Match Level</h3>
                    <p className={`text-2xl font-bold mt-1 ${
                      result.match_level === "High" ? "text-green-400" :
                      result.match_level === "Medium" ? "text-yellow-400" : "text-red-400"
                    }`}>
                      {result.match_level}
                    </p>
                  </div>
                </div>

                {/* Vertical Divider for Desktop */}
                <div className="hidden md:block w-px h-full bg-white/10 mx-auto"></div>

                {/* Missing Skills */}
                <div>
                   <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                    <span className="text-red-400">⚠</span> Missing Skills
                   </h3>
                   <div className="flex flex-wrap gap-2">
                    {result.missing_skills.length > 0 ? (
                      result.missing_skills.map((skill: string) => (
                        <span key={skill} className="px-3 py-1 bg-red-500/20 text-red-200 border border-red-500/30 rounded-lg text-sm">
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="text-green-400 italic text-sm">No missing skills detected!</span>
                    )}
                   </div>
                </div>

              </div>

              {/* Suggestions */}
              <div className="mt-8 pt-8 border-t border-white/10">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <span className="text-blue-400">💡</span> Suggestions for Improvement
                </h3>
                <div className="grid gap-3">
                  {result.suggestions.map((s: string, i: number) => (
                    <div key={i} className="flex gap-3 p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-100 text-sm">
                      <span className="shrink-0 mt-0.5">•</span>
                      <span>{s}</span>
                    </div>
                  ))}
                </div>
              </div>
              
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
