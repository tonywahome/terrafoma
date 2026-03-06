import Image from "next/image";
import Link from "next/link";
import StatsBar from "@/components/StatsBar";
import HeroVideo from "@/components/HeroVideo";

export default function Home() {
  return (
    <div>
      {/* Hero + StatsBar — one unified video-backed block */}
      <section className="relative text-white overflow-hidden">
        {/* Video background stretches behind navbar (fixed) + hero + statsbar */}
        <HeroVideo />

        {/* pt-16 clears the fixed navbar (h-16) */}
        <div className="relative pt-16">
          <div className="max-w-7xl mx-auto px-4 py-28 text-center">
            <h1 className="animate-fade-up text-5xl font-bold mb-4 drop-shadow-lg">
              TerraFoma
            </h1>
            <p className="animate-fade-up-delay-1 text-xl text-white/85 mb-8 max-w-2xl mx-auto drop-shadow">
              Empowering local economies through transparent, AI-verified
              natural capital. Connecting land stewards with local emitters.
            </p>
            <div className="animate-fade-up-delay-2 flex gap-4 justify-center">
              <Link
                href="/scan"
                className="bg-white text-terra-700 px-6 py-3 rounded-lg font-semibold hover:bg-terra-50 transition-colors duration-200"
              >
                Scan Land
              </Link>
              <Link
                href="/marketplace"
                className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/15 transition-colors duration-200"
              >
                Buy Credits
              </Link>
            </div>
          </div>

          {/* Stats ribbon — glassy, sits on the video */}
          <StatsBar glassy />
        </div>
      </section>

      {/* Features */}
      <section className="relative py-16 overflow-hidden">
        <div className="absolute inset-0">
          <Image
            src="/forest-bg.jpg"
            alt="Forest background"
            fill
            className="object-cover"
          />
          <div className="absolute inset-0 bg-black/65" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-white">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-colors duration-200">
              <div className="w-12 h-12 bg-terra-600/80 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🛰️</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">
                AI-Powered Scanning
              </h3>
              <p className="text-white/75">
                Our AI analyzes satellite imagery to estimate carbon stock,
                biomass, and generate an integrity score for every plot.
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-colors duration-200">
              <div className="w-12 h-12 bg-terra-600/80 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">
                Transparent Registry
              </h3>
              <p className="text-white/75">
                Every credit has a full audit trail from verification to
                retirement, with integrity scores and risk assessments.
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-colors duration-200">
              <div className="w-12 h-12 bg-terra-600/80 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🏭</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">
                Local Offsetting
              </h3>
              <p className="text-white/75">
                SMEs buy credits from nearby conservation projects, keeping the
                &quot;green dollar&quot; in the local economy.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-16 overflow-hidden">
        <div className="absolute inset-0">
          <Image
            src="/forest-bg.jpg"
            alt="Forest background"
            fill
            className="object-cover object-bottom"
          />
          <div className="absolute inset-0 bg-black/60" />
        </div>

        <div className="relative max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4 text-white">
            Ready to Make an Impact?
          </h2>
          <p className="text-white/80 mb-8">
            Whether you&apos;re a landowner looking to monetize your
            conservation efforts or a business seeking verified local offsets,
            TerraFoma makes it simple.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/scan"
              className="bg-terra-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-terra-700 transition-colors duration-200"
            >
              I&apos;m a Landowner
            </Link>
            <Link
              href="/dashboard"
              className="bg-white text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200"
            >
              I&apos;m a Business
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
