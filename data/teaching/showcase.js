// Progressive enhancement for the teaching examples. Replays contain only SVG frames.
(() => {
  document.querySelectorAll('.demo-switch').forEach(group => {
    const frame = document.getElementById(group.dataset.frame);
    const caption = document.getElementById(group.dataset.caption);
    const fullView = document.getElementById(group.dataset.fullView);
    group.addEventListener('click', event => {
      const link = event.target.closest('a[data-title]');
      if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (link.getAttribute('aria-current') === 'true') return;
      group.querySelectorAll('a').forEach(item => item.removeAttribute('aria-current'));
      link.setAttribute('aria-current', 'true');
      frame.title = link.dataset.title;
      frame.src = link.href;
      caption.textContent = link.dataset.caption;
      fullView.href = link.href;
    });
  });

  document.querySelectorAll('iframe.replay').forEach(frame => {
    let resizeObserver;
    const fitReplay = () => {
      resizeObserver?.disconnect();
      const body = frame.contentDocument?.body;
      if (!body) return;
      frame.contentDocument.documentElement.style.overflow = 'hidden';
      const resize = () => { frame.style.height = `${Math.ceil(body.getBoundingClientRect().height) + 8}px`; };
      resizeObserver = new ResizeObserver(resize);
      resizeObserver.observe(body);
      resize();
    };
    frame.addEventListener('load', fitReplay);
    if (frame.contentDocument?.readyState === 'complete' && frame.contentDocument.URL !== 'about:blank') fitReplay();
    const visibility = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) frame.contentWindow?.postMessage('pause-replay', location.origin);
    });
    visibility.observe(frame);
  });

  const next = document.getElementById('next-sample');
  const sample = document.getElementById('gpt-sample');
  if (next && sample) {
    let samples;
    let sampleIndex = 0;
    // Leave the first recorded excerpt readable if JavaScript or loading is unavailable.
    fetch('/data/teaching/showcase/gpt-samples.json')
      .then(response => {
        if (!response.ok) throw new Error('Samples unavailable');
        return response.json();
      })
      .then(value => { samples = value; next.hidden = false; })
      .catch(() => {});
    next.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      sampleIndex = (sampleIndex + 1) % samples.length;
      sample.textContent = samples[sampleIndex];
    });
  }

  // Keep comparisons audible when moving between the original and reconstructed clips.
  const audioClips = document.querySelectorAll('audio');
  audioClips.forEach(clip => clip.addEventListener('play', () => {
    audioClips.forEach(other => { if (other !== clip) other.pause(); });
  }));

  function revealArchiveLink() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    const archive = target?.closest('details');
    if (archive) {
      archive.open = true;
      target.scrollIntoView();
    }
  }
  window.addEventListener('hashchange', revealArchiveLink);
  revealArchiveLink();
})();
