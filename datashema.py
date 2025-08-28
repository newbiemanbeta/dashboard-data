from sqlalchemy import (
    Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# --- Master tables (lookups) ---

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)   # e.g., 'Meta', 'Google', 'TikTok', 'Shopify'

    campaigns = relationship("Campaign", back_populates="platform")


class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    campaign_name = Column(String, nullable=False)

    platform = relationship("Platform", back_populates="campaigns")
    adsets = relationship("AdSet", back_populates="campaign")


class AdSet(Base):
    __tablename__ = "adsets"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    adset_name = Column(String, nullable=False)

    campaign = relationship("Campaign", back_populates="adsets")
    ads = relationship("Ad", back_populates="adset")


class Ad(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True)
    adset_id = Column(Integer, ForeignKey("adsets.id"), nullable=False)
    ad_name = Column(String, nullable=False)

    adset = relationship("AdSet", back_populates="ads")
    metrics = relationship("PerformanceMetric", back_populates="ad")


# --- Fact table: daily performance metrics ---

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    id = Column(Integer, primary_key=True)
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=False)
    date = Column(Date, nullable=False)

    # Spend & delivery
    spend = Column(Float, default=0)
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    frequency = Column(Float, default=0)

    # Engagement
    clicks = Column(Integer, default=0)
    ctr = Column(Float, default=0)   # CTR = Clicks / Impressions
    video_views = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0)

    # Conversions (ad events)
    add_to_cart = Column(Integer, default=0)
    checkout = Column(Integer, default=0)
    purchases = Column(Integer, default=0)

    # Shopify / revenue
    revenue = Column(Float, default=0)
    aov = Column(Float, default=0)   # Avg. Order Value
    roas = Column(Float, default=0)  # Return on Ad Spend
    mer = Column(Float, default=0)   # Marketing Efficiency Ratio

    ad = relationship("Ad", back_populates="metrics")

    __table_args__ = (
        UniqueConstraint("ad_id", "date", name="uix_ad_date"),  # avoid duplicates
    )

# --- Daily Channel Summary ---
class DailyChannelSummary(Base):
    __tablename__ = "daily_channel_summary"
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    date = Column(Date, nullable=False)

    spend = Column(Float, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    revenue = Column(Float, default=0)

    roas = Column(Float, default=0)   # Return on Ad Spend
    mer = Column(Float, default=0)    # Marketing Efficiency Ratio

    platform = relationship("Platform")

    __table_args__ = (
        UniqueConstraint("platform_id", "date", name="uix_platform_date"),
    )


# --- Weekly Ad Summary ---
class WeeklyAdSummary(Base):
    __tablename__ = "weekly_ad_summary"
    id = Column(Integer, primary_key=True)
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=False)
    week_start = Column(Date, nullable=False)   # Monday start
    week_end = Column(Date, nullable=False)     # Sunday end

    spend = Column(Float, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    revenue = Column(Float, default=0)

    roas = Column(Float, default=0)
    mer = Column(Float, default=0)

    # AI agent recommendations for that ad (JSON/text)
    ai_analysis = Column(String)  

    ad = relationship("Ad")

    __table_args__ = (
        UniqueConstraint("ad_id", "week_start", "week_end", name="uix_ad_week"),
    )


# --- Weekly Channel Summary ---
class WeeklyChannelSummary(Base):
    __tablename__ = "weekly_channel_summary"
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    week_start = Column(Date, nullable=False)
    week_end = Column(Date, nullable=False)

    spend = Column(Float, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    purchases = Column(Integer, default=0)
    revenue = Column(Float, default=0)

    roas = Column(Float, default=0)
    mer = Column(Float, default=0)

    # AI agent insights per channel/week
    ai_analysis = Column(String)  

    platform = relationship("Platform")

    __table_args__ = (
        UniqueConstraint("platform_id", "week_start", "week_end", name="uix_platform_week"),
    )
