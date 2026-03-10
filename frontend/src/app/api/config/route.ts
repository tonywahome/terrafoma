import { NextResponse } from "next/server";

export async function GET() {
  // Serve runtime config to the client — token is read server-side from env,
  // so it never needs to be baked into the JS bundle at build time.
  return NextResponse.json({
    mapboxToken: process.env.NEXT_PUBLIC_MAPBOX_TOKEN || process.env.MAPBOX_TOKEN || "",
  });
}
