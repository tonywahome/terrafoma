import { NextResponse } from "next/server";

export async function GET() {
  // Serve runtime config to the client — token is read server-side from env,
  // so it never needs to be baked into the JS bundle at build time.
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || process.env.MAPBOX_TOKEN || "";
  
  console.log('Config API called - Token available:', !!token);
  console.log('NEXT_PUBLIC_MAPBOX_TOKEN exists:', !!process.env.NEXT_PUBLIC_MAPBOX_TOKEN);
  
  return NextResponse.json({
    mapboxToken: token,
  });
}
