import { ReactNode } from "react";
import { SalesIQLoader } from "./SalesIQLoader";

type LayoutProps = {
  children: ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <>
      {/* ✅ Load SalesIQ only when this layout is used (after login) */}
      <SalesIQLoader />

      <div className="min-h-screen flex bg-slate-100">
        {/* Sidebar */}
        <aside className="w-64 bg-slate-950 text-slate-50 flex flex-col">
          <div className="px-6 py-4 border-b border-slate-800">
            <h1 className="text-xl font-semibold tracking-tight">
              DermaVision
            </h1>
          </div>
          <nav className="flex-1 px-2 py-4 space-y-1 text-sm">
            {/* These labels are just visual.
                Actual navigation is handled by your router pages */}
            <div className="px-3 py-2 rounded-md bg-slate-900/60">
              Dashboard
            </div>
            <div className="px-3 py-2 rounded-md hover:bg-slate-900/40">
              Skin Scan
            </div>
            <div className="px-3 py-2 rounded-md hover:bg-slate-900/40">
              Disease Tips
            </div>
            <div className="px-3 py-2 rounded-md hover:bg-slate-900/40">
              History
            </div>
            <div className="px-3 py-2 rounded-md hover:bg-slate-900/40">
              Doctor Consult
            </div>
            <div className="px-3 py-2 rounded-md hover:bg-slate-900/40">
              Calendar
            </div>
            <div className="px-3 py-2 rounded-md hover:bg-slate-900/40">
              Profile
            </div>
          </nav>
        </aside>

        {/* Main content */}
        <main className="flex-1 min-h-screen">
          {children}
        </main>
      </div>
    </>
  );
}
