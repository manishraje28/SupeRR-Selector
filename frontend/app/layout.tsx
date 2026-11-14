import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SupeRR Selector | Rajasthan Royals IPL 2027 Auction War Room",
  description: "Official Pressure Intelligence Suite for identifying the most reliable T20 players under pressure.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased dark">
      <body className="min-h-full flex flex-col bg-[#070B14] text-slate-100 font-sans">
        {children}
      </body>
    </html>
  );
}
