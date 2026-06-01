import { useEffect, useState, useMemo } from 'react';

function fitClass(score) {
  if (score >= 90) return 'high';
  if (score >= 80) return 'mid';
  return 'low';
}

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('./jobs.json')
      .then((r) => {
        if (!r.ok) throw new Error(`Failed to load jobs (${r.status})`);
        return r.json();
      })
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  const jobs = data?.jobs ?? [];
  const stats = useMemo(() => {
    if (!jobs.length) return { total: 0, perfect: 0, newToday: 0 };
    return {
      total: jobs.length,
      perfect: jobs.filter((j) => j.fitScore >= 90).length,
      newToday: jobs.filter((j) => j.isNew).length,
    };
  }, [jobs]);

  if (error) {
    return (
      <div className="app">
        <p className="error">Could not load dashboard: {error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="app">
        <p className="loading">Loading Job Command Centre…</p>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Job Command Centre</h1>
        <p className="name">{data.profile?.name ?? 'Abhishek Kumar'}</p>
        <p className="tagline">AI-Powered Job Matching · Updated automatically</p>
      </header>

      <main className="content">
        <section className="stats">
          <div>
            <span className="stat-value green">{stats.total}</span>
            <span className="stat-label">Jobs Found</span>
          </div>
          <div>
            <span className="stat-value green">{stats.perfect}</span>
            <span className="stat-label">Perfect Match</span>
          </div>
          <div>
            <span className="stat-value red">{stats.newToday}</span>
            <span className="stat-label">New Today</span>
          </div>
        </section>

        {data.updatedAt && (
          <p className="meta">Last updated: {new Date(data.updatedAt).toLocaleString('en-IN')}</p>
        )}

        <div className="jobs">
          {jobs.map((job) => (
            <article
              key={job.id}
              className={`job-card ${job.fitScore >= 90 ? 'high' : ''} ${job.isHot ? 'hot' : ''}`}
            >
              <div>
                <div className="job-title-row">
                  <h2 className="job-title">{job.title}</h2>
                  {job.isNew && <span className="badge">New</span>}
                  {job.isHot && <span className="badge">Hot</span>}
                </div>
                <div className="job-meta">
                  <span>{job.company}</span>
                  <span>{job.location}</span>
                  <span className="salary">{job.salary}</span>
                </div>
              </div>
              <div className="job-actions">
                <div className={`fit ${fitClass(job.fitScore)}`}>
                  {job.fitScore}
                  <span>FIT</span>
                </div>
                <a
                  className="apply-btn"
                  href={job.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Apply
                </a>
              </div>
            </article>
          ))}
        </div>
      </main>
    </div>
  );
}
