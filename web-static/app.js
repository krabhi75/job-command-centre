function fitClass(score) {
  if (score >= 90) return 'high';
  if (score >= 80) return 'mid';
  return 'low';
}

async function init() {
  const jobsEl = document.getElementById('jobs');
  const statsEl = document.getElementById('stats');
  const metaEl = document.getElementById('meta');

  try {
    const res = await fetch('./jobs.json');
    if (!res.ok) throw new Error('Could not load jobs.json');
    const data = await res.json();
    const jobs = data.jobs || [];
    const perfect = jobs.filter((j) => j.fitScore >= 90).length;
    const newToday = jobs.filter((j) => j.isNew).length;

    statsEl.innerHTML = `
      <div><span class="stat-value green">${jobs.length}</span><span class="stat-label">Jobs Found</span></div>
      <div><span class="stat-value green">${perfect}</span><span class="stat-label">Perfect Match</span></div>
      <div><span class="stat-value red">${newToday}</span><span class="stat-label">New Today</span></div>
    `;

    const parts = [];
    if (data.updatedAt) parts.push('Updated: ' + new Date(data.updatedAt).toLocaleString('en-IN'));
    if (data.sourcesScraped?.length) parts.push('Sources: ' + data.sourcesScraped.join(', '));
    if (parts.length) metaEl.textContent = parts.join(' · ');

    jobsEl.innerHTML = jobs
      .map(
        (job) => `
      <article class="job-card ${job.fitScore >= 90 ? 'high' : ''} ${job.isHot ? 'hot' : ''}">
        <div>
          <div class="job-title-row">
            <h2 class="job-title">${job.title}</h2>
            ${job.isNew ? '<span class="badge">New</span>' : ''}
            ${job.isHot ? '<span class="badge">Hot</span>' : ''}
          </div>
          <div class="job-meta">
            <span>${job.company}</span>
            <span>${job.location}</span>
            <span class="salary">${job.salary}</span>
            ${job.source ? `<span style="opacity:0.65">${job.source}</span>` : ''}
          </div>
        </div>
        <div class="job-actions">
          <div class="fit ${fitClass(job.fitScore)}">${job.fitScore}<span>FIT</span></div>
          <a class="apply-btn" href="${job.url}" target="_blank" rel="noopener">Apply</a>
        </div>
      </article>`
      )
      .join('');
  } catch (e) {
    jobsEl.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

init();
