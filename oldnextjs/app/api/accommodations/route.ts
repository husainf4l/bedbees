import { NextRequest, NextResponse } from 'next/server';
import { Apartment } from '@/types/common';

// In-memory storage for demo purposes
// In production, this would be a database
const accommodations: Apartment[] = [];

export async function GET() {
  try {
    // Return all accommodations
    return NextResponse.json({
      success: true,
      data: accommodations
    });
  } catch (error) {
    console.error('Error fetching accommodations:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch accommodations' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    const requiredFields = ['title', 'description', 'city', 'country', 'basePrice', 'maxGuests'];
    for (const field of requiredFields) {
      if (!body[field]) {
        return NextResponse.json(
          { success: false, error: `Missing required field: ${field}` },
          { status: 400 }
        );
      }
    }

    // Create new accommodation
    const newAccommodation: Apartment = {
      id: Date.now().toString(),
      title: body.title,
      description: body.description,
      categoryId: body.categoryId || 'default',
      hostId: body.hostId || 'current-user', // In real app, get from auth
      city: body.city,
      country: body.country,
      address: body.address || '',
      latitude: body.latitude || 0,
      longitude: body.longitude || 0,
      basePrice: body.basePrice,
      currency: body.currency || 'USD',
      maxGuests: body.maxGuests,
      bedrooms: body.bedrooms || 1,
      bathrooms: body.bathrooms || 1,
      amenities: body.amenities || [],
      images: body.images || [],
      isAvailable: true,
      status: 'active',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      host: {
        id: body.hostId || 'current-user',
        name: body.hostName || 'Host',
        email: body.hostEmail || 'host@example.com',
        image: body.hostImage || null
      },
      category: {
        id: body.categoryId || 'default',
        type: body.categoryType || 'apartment',
        title: body.categoryTitle || 'Accommodation',
        subtitle: body.categorySubtitle || 'A place to stay',
        image: body.categoryImage || '/hero/apartment.webp',
        sectionTitle: body.categorySectionTitle || 'Accommodations',
        message: body.categoryMessage || 'Find your perfect place to stay',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    };

    // Add to in-memory storage
    accommodations.push(newAccommodation);

    return NextResponse.json({
      success: true,
      data: newAccommodation
    }, { status: 201 });

  } catch (error) {
    console.error('Error creating accommodation:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to create accommodation' },
      { status: 500 }
    );
  }
}