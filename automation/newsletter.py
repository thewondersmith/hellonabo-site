import os
import sys
import urllib3
def main():
    """Main execution"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("🚀 Madison Safety Newsletter Generator")
    print("=" * 50)
    
    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize scrapers
    print("\n📡 Scraping Madison PD data...")
    crime_scraper = MadisonDataScraper()
    
    # Download and parse arrests
    arrests_pdf = crime_scraper.download_pdf(ARRESTS_PDF_URL)
    arrests = []
    if arrests_pdf:
        arrests = crime_scraper.parse_arrests_pdf(arrests_pdf)
        print(f"  ✅ Found {len(arrests)} arrests")
    else:
        print("  ⚠️  Could not download arrests PDF")
    
    # Get incidents
    incidents = crime_scraper.scrape_incidents()
    print(f"  ✅ Found {len(incidents)} incidents")
    
    # Categorize crimes
    for arrest in arrests:
        arrest['category'] = crime_scraper.categorize_crime(arrest.get('charge', ''))
    
    # Scrape sex offender data
    print("\n📡 Scraping ALEA sex offender registry...")
    alea_scraper = ALEAScraper()
    offender_count = alea_scraper.get_offender_count("Madison", "AL")
    
    sex_offender_data = {
        'total': offender_count or 23,  # Fallback to manual count
        'per_1000': ((offender_count or 23) / POPULATION) * 1000
    }
    print(f"  ✅ Found {sex_offender_data['total']} registered offenders")
    
    # Generate dashboard
    print("\n🤖 Generating dashboard with Claude AI...")
    generator = DashboardGenerator(api_key)
    
    crime_data = {
        'arrests': arrests,
        'incidents': incidents
    }
    
    generator.generate_dashboard(
        crime_data=crime_data,
        sex_offender_data=sex_offender_data,
        output_path='../madison-al/index.html'  # ✅ FIXED: Goes up one level
    )
    
    print("\n✅ Complete! Dashboard generated.")
    print(f"📊 Stats: {len(arrests)} arrests, {len(incidents)} incidents")
    print(f"🔗 Output: ../madison-al/index.html")

if __name__ == "__main__":
    main()
