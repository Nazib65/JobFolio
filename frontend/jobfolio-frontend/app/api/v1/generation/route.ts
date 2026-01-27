import { NextRequest, NextResponse } from 'next/server';

export const maxDuration = 120; // 2 minutes (max for Vercel Hobby, adjust as needed)
export const dynamic = 'force-dynamic';

export async function POST(request: NextRequest) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minutes
  
  try {
    const body = await request.json();
    
    // Proxy the request to the FastAPI backend
    const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
    const response = await fetch(`${backendUrl}/api/v1/generation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: errorText || 'Generation failed' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    clearTimeout(timeoutId);
    console.error('Generation proxy error:', error);
    
    if (error.name === 'TimeoutError' || error.name === 'AbortError' || controller.signal.aborted) {
      return NextResponse.json(
        { error: 'Request timeout - generation took too long' },
        { status: 504 }
      );
    }
    
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}
