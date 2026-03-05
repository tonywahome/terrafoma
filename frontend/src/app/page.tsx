import Link from "next/link";
import StatsBar from "@/components/StatsBar";

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-terra-700 to-terra-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">TerraFoma</h1>
          <p className="text-xl text-terra-200 mb-8 max-w-2xl mx-auto">
            Empowering local economies through transparent, AI-verified natural
            capital. Connecting land stewards with local emitters.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/scan"
              className="bg-white text-terra-700 px-6 py-3 rounded-lg font-semibold hover:bg-terra-50 transition"
            >
              Scan Land
            </Link>
            <Link
              href="/marketplace"
              className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10 transition"
            >
              Buy Credits
            </Link>
          </div>
        </div>
      </section>

      <StatsBar />

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
          How It Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <div className="w-12 h-12 bg-terra-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🛰️</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">AI-Powered Scanning</h3>
            <p className="text-gray-600">
              Our AI analyzes satellite imagery to estimate carbon stock,
              biomass, and generate an integrity score for every plot.
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <div className="w-12 h-12 bg-terra-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">
              Transparent Registry
            </h3>
            <p className="text-gray-600">
              Every credit has a full audit trail from verification to
              retirement, with integrity scores and risk assessments.
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <div className="w-12 h-12 bg-terra-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🏭</span>
            </div>
            <h3 className="text-xl font-semibold mb-2">Local Offsetting</h3>
            <p className="text-gray-600">
              SMEs buy credits from nearby conservation projects, keeping the
              &quot;green dollar&quot; in the local economy.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-terra-50 py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4 text-gray-900">
            Ready to Make an Impact?
          </h2>
          <p className="text-gray-600 mb-8">
            Whether you&apos;re a landowner looking to monetize your
            conservation efforts or a business seeking verified local offsets,
            TerraFoma makes it simple.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/scan"
              className="bg-terra-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-terra-700 transition"
            >
              I&apos;m a Landowner
            </Link>
            <Link
              href="/dashboard"
              className="bg-gray-800 text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-900 transition"
            >
              I&apos;m a Business
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
