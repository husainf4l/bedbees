import { NextRequest, NextResponse } from 'next/server';
import { Tour } from '@/types/tour';

// In-memory storage for demo purposes
// In production, this would be a database
const tours: Tour[] = [];

export async function GET() {
  try {
    // Return all tours
    return NextResponse.json({
      success: true,
      data: tours
    });
  } catch (error) {
    console.error('Error fetching tours:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch tours' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    const requiredFields = ['title', 'description', 'city', 'country', 'basePrice', 'maxParticipants'];
    for (const field of requiredFields) {
      if (!body[field]) {
        return NextResponse.json(
          { success: false, error: `Missing required field: ${field}` },
          { status: 400 }
        );
      }
    }

    // Create new tour
    const newTour: Tour = {
      id: Date.now().toString(),
      guideId: body.guideId || 'current-user', // In real app, get from auth
      title: body.title,
      description: body.description || '',
      city: body.city,
      country: body.country,
      category: body.category || 'general',
      startTimes: body.startTimes || [],
      basePrice: body.basePrice,
      currency: body.currency || 'USD',
      minGroup: body.minGroup || 1,
      maxGroup: body.maxGroup || body.maxParticipants || 10,
      durationMins: body.durationMins || body.duration || 60,
      language: body.language || 'English',
      languages: body.languages || ['English'],
      isPayWhatYouWant: body.isPayWhatYouWant || false,
      status: 'active',
      createdAt: new Date().toISOString(),

      // Enhanced filtering fields
      travelStyles: body.travelStyles || [],
      accessibility: body.accessibility || [],
      startWindow: body.startWindow,
      instantBook: body.instantBook || false,
      cancellationPolicy: body.cancellationPolicy || 'flexible',

      // Deal states
      isDropIn: body.isDropIn || false,
      isEarlyBird: body.isEarlyBird || false,

      // Location details
      latitude: body.latitude || null,
      longitude: body.longitude || null,
      meetingPoint: body.meetingPoint,

      // SEO and searchability
      tags: body.tags || [],
      searchKeywords: body.searchKeywords || [],

      // Tour details
      highlights: body.highlights || [],
      difficulty: body.difficulty || 'easy',
      whatsIncluded: body.whatsIncluded || [],
      whatsExcluded: body.whatsExcluded || [],
      requirements: body.requirements || [],
      itinerary: body.itinerary || '',

      // Relations
      guide: {
        id: body.guideId || 'current-user',
        userId: body.guideId || 'current-user',
        bio: body.guideBio || null,
        kycStatus: 'verified',
        ratingAvg: 4.5,
        toursCount: 1,
        user: {
          id: body.guideId || 'current-user',
          name: body.guideName || 'Guide',
          email: body.guideEmail || 'guide@example.com',
          image: body.guideImage || null
        }
      },
      media: body.media || [],
      _count: {
        bookings: 0
      }
    };

    // Add to in-memory storage
    tours.push(newTour);

    return NextResponse.json({
      success: true,
      data: newTour
    }, { status: 201 });

  } catch (error) {
    console.error('Error creating tour:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to create tour' },
      { status: 500 }
    );
  }
}