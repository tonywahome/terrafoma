import { NextResponse } from "next/server";

export async function GET() {
  // Serve runtime config to the client — token is read server-side from env,
  // so it never needs to be baked into the JS bundle at build time.
  const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || process.env.MAPBOX_TOKEN || "";
  
  // Comprehensive debugging for Railway
  console.log('=== CONFIG API DEBUG ===');
  console.log('NEXT_PUBLIC_MAPBOX_TOKEN exists:', !!process.env.NEXT_PUBLIC_MAPBOX_TOKEN);
  console.log('MAPBOX_TOKEN exists:', !!process.env.MAPBOX_TOKEN);
  console.log('Token length:', token.length);
  console.log('Token preview:', token ? `${token.substring(0, 15)}...` : 'EMPTY');
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('RAILWAY_ENVIRONMENT:', process.env.RAILWAY_ENVIRONMENT);
  console.log('All env vars starting with NEXT_PUBLIC:', 
    Object.keys(process.env)
      .filter(key => key.startsWith('NEXT_PUBLIC'))
      .map(key => `${key}=${process.env[key] ? 'SET' : 'UNSET'}`)
  );
  console.log('========================');
  
  if (!token) {
    console.error('❌ CRITICAL: Mapbox token not found in environment variables!');
    console.error('Please set NEXT_PUBLIC_MAPBOX_TOKEN in Railway dashboard');
  }
  
  return NextResponse.json({
    mapboxToken: token,
    debug: {
      hasToken: !!token,
      tokenLength: token.length,
      environment: process.env.NODE_ENV,
      railway: !!process.env.RAILWAY_ENVIRONMENT
    }
  });
}
