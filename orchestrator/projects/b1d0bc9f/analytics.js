// Analytics Tracking
class Analytics {
  static track(event, data = {}) {
    console.log(`[Analytics] ${event}`, data);
    // Send to analytics service
  }
  
  static pageView(page) {
    this.track('page_view', { page });
  }
}

export default Analytics;
