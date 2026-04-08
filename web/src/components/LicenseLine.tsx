// Single source of truth for the dual-license + citation footer note.
// Code is MIT; content (patterns, docs, paper, prose) is CC BY 4.0;
// academic citation lives in CITATION.cff which GitHub renders as a
// "Cite this repository" button. Keeping all three references here
// means HomePage and DocsPage can never drift apart.
export function LicenseLine() {
  return (
    <p className="text-xs text-zinc-600">
      Code{' '}
      <a
        href="https://github.com/emergent-wisdom/sema/blob/main/LICENSE"
        target="_blank"
        rel="noopener noreferrer"
        className="underline decoration-zinc-700 underline-offset-2 hover:decoration-emerald-500/60 hover:text-zinc-400 transition-colors"
      >
        MIT
      </a>{' '}
      ·{' '}
      Content{' '}
      <a
        href="https://creativecommons.org/licenses/by/4.0/"
        target="_blank"
        rel="noopener noreferrer"
        className="underline decoration-zinc-700 underline-offset-2 hover:decoration-emerald-500/60 hover:text-zinc-400 transition-colors"
      >
        CC BY 4.0
      </a>{' '}
      ·{' '}
      <a
        href="https://github.com/emergent-wisdom/sema#citing"
        target="_blank"
        rel="noopener noreferrer"
        className="underline decoration-zinc-700 underline-offset-2 hover:decoration-emerald-500/60 hover:text-zinc-400 transition-colors"
      >
        Cite this work
      </a>
    </p>
  );
}
