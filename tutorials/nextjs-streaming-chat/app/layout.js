import "./globals.css";

export const metadata = { title: "Streaming chat" };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
