import type { ReactNode } from 'react';

interface DashboardGridProps {
  children: ReactNode;
}

export default function DashboardGrid({ children }: DashboardGridProps) {
  return (
    <div className="max-w-screen-2xl mx-auto px-4 py-4 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      {children}
    </div>
  );
}
