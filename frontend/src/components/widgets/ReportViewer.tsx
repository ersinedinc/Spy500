import { useState } from 'react';
import Markdown from 'react-markdown';
import { useTranslation } from '../../i18n';

interface ReportViewerProps {
  markdown: string;
}

export default function ReportViewer({ markdown }: ReportViewerProps) {
  const [copied, setCopied] = useState(false);
  const { t } = useTranslation();

  const handleCopy = async () => {
    await navigator.clipboard.writeText(markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
      <div className="flex justify-between items-center mb-3">
        <div className="text-sm font-medium text-gray-300">{t('report.title')}</div>
        <button
          onClick={handleCopy}
          className="px-2 py-1 text-xs bg-gray-800 hover:bg-gray-700 text-gray-400 rounded border border-gray-700 transition-colors"
        >
          {copied ? t('report.copied') : t('report.copy')}
        </button>
      </div>
      <div className="prose prose-sm prose-invert max-w-none text-gray-300
        prose-headings:text-gray-200 prose-strong:text-gray-200
        prose-table:text-xs prose-th:text-gray-400 prose-td:text-gray-400
        prose-blockquote:border-yellow-600 prose-blockquote:text-yellow-200/80
      ">
        <Markdown>{markdown}</Markdown>
      </div>
    </div>
  );
}
