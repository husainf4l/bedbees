# Generated manually for photo gallery fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_accommodation_bed_type_and_more'),
    ]

    operations = [
        # Rename fields for AccommodationPhoto
        migrations.RenameField(
            model_name='accommodationphoto',
            old_name='image',
            new_name='original_file',
        ),
        migrations.RenameField(
            model_name='accommodationphoto',
            old_name='order',
            new_name='display_order',
        ),
        migrations.RenameField(
            model_name='accommodationphoto',
            old_name='is_primary',
            new_name='is_hero',
        ),

        # Rename fields for TourPhoto
        migrations.RenameField(
            model_name='tourphoto',
            old_name='image',
            new_name='original_file',
        ),
        migrations.RenameField(
            model_name='tourphoto',
            old_name='order',
            new_name='display_order',
        ),
        migrations.RenameField(
            model_name='tourphoto',
            old_name='is_primary',
            new_name='is_hero',
        ),

        # Add new fields to AccommodationPhoto
        migrations.AddField(
            model_name='accommodationphoto',
            name='alt_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='attribution',
            field=models.CharField(blank=True, help_text='Photographer or source', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='exif_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='file_size',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='large',
            field=models.ImageField(blank=True, null=True, upload_to='accommodations/gallery/large/'),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('360', '360° Image')], default='image', max_length=10),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='medium',
            field=models.ImageField(blank=True, null=True, upload_to='accommodations/gallery/medium/'),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='mime_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='nsfw_rating',
            field=models.CharField(choices=[('safe', 'Safe'), ('mild', 'Mild NSFW'), ('adult', 'Adult Content')], default='safe', max_length=10),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='small',
            field=models.ImageField(blank=True, null=True, upload_to='accommodations/gallery/small/'),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated tags', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='accommodations/gallery/thumbs/'),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='video_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='video_thumbnail_time',
            field=models.FloatField(default=0, help_text='Time in seconds for video thumbnail'),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('hidden', 'Hidden'), ('private', 'Private')], default='public', max_length=10),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='xl',
            field=models.ImageField(blank=True, null=True, upload_to='accommodations/gallery/xl/'),
        ),
        migrations.AddField(
            model_name='accommodationphoto',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),

        # Add new fields to TourPhoto
        migrations.AddField(
            model_name='tourphoto',
            name='alt_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='attribution',
            field=models.CharField(blank=True, help_text='Photographer or source', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='exif_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='file_size',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='large',
            field=models.ImageField(blank=True, null=True, upload_to='tours/gallery/large/'),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('360', '360° Image')], default='image', max_length=10),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='medium',
            field=models.ImageField(blank=True, null=True, upload_to='tours/gallery/medium/'),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='mime_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='nsfw_rating',
            field=models.CharField(choices=[('safe', 'Safe'), ('mild', 'Mild NSFW'), ('adult', 'Adult Content')], default='safe', max_length=10),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='small',
            field=models.ImageField(blank=True, null=True, upload_to='tours/gallery/small/'),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated tags', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='tours/gallery/thumbs/'),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='video_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='video_thumbnail_time',
            field=models.FloatField(default=0, help_text='Time in seconds for video thumbnail'),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('hidden', 'Hidden'), ('private', 'Private')], default='public', max_length=10),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='xl',
            field=models.ImageField(blank=True, null=True, upload_to='tours/gallery/xl/'),
        ),
        migrations.AddField(
            model_name='tourphoto',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),

        # Update ordering for AccommodationPhoto
        migrations.AlterModelOptions(
            name='accommodationphoto',
            options={'ordering': ['display_order', '-uploaded_at']},
        ),

        # Update ordering for TourPhoto
        migrations.AlterModelOptions(
            name='tourphoto',
            options={'ordering': ['display_order', '-uploaded_at']},
        ),

        # Add indexes for better performance
        migrations.AddIndex(
            model_name='accommodationphoto',
            index=models.Index(fields=['accommodation', 'display_order'], name='core_accommod_display_order_idx'),
        ),
        migrations.AddIndex(
            model_name='accommodationphoto',
            index=models.Index(fields=['accommodation', 'is_hero'], name='core_accommod_is_hero_idx'),
        ),
        migrations.AddIndex(
            model_name='accommodationphoto',
            index=models.Index(fields=['accommodation', 'visibility'], name='core_accommod_visibility_idx'),
        ),
        migrations.AddIndex(
            model_name='accommodationphoto',
            index=models.Index(fields=['media_type'], name='core_accommod_media_type_idx'),
        ),

        migrations.AddIndex(
            model_name='tourphoto',
            index=models.Index(fields=['tour', 'display_order'], name='core_tourphoto_display_order_idx'),
        ),
        migrations.AddIndex(
            model_name='tourphoto',
            index=models.Index(fields=['tour', 'is_hero'], name='core_tourphoto_is_hero_idx'),
        ),
        migrations.AddIndex(
            model_name='tourphoto',
            index=models.Index(fields=['tour', 'visibility'], name='core_tourphoto_visibility_idx'),
        ),
        migrations.AddIndex(
            model_name='tourphoto',
            index=models.Index(fields=['media_type'], name='core_tourphoto_media_type_idx'),
        ),
    ]
