# ======================================================================================
# ZI AUTONOMOUS AGENT SYSTEM - SEO AUTO-OPTIMIZATION ENGINE
# ======================================================================================
# High-impact growth feature for organic search discoverability
# Automatically optimizes content for search engines and platforms
# ======================================================================================

import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import Counter
import requests

# ======================================================================================
# DATA STRUCTURES
# ======================================================================================

@dataclass
class SEOScore:
    """SEO score with breakdown"""
    overall_score: float
    title_score: float
    description_score: float
    content_score: float
    technical_score: float
    suggestions: List[str]

@dataclass
class KeywordData:
    """Keyword analysis data"""
    keyword: str
    density: float
    prominence: float
    difficulty: float
    volume: int  # Estimated search volume
    suggestions: List[str]

@dataclass
class OptimizedContent:
    """SEO-optimized content"""
    title: str
    description: str
    content: str
    keywords: List[str]
    tags: List[str]
    canonical_url: str
    schema_markup: str
    meta_tags: Dict[str, str]
    seo_score: SEOScore

# ======================================================================================
# SEO OPTIMIZER ENGINE
# ======================================================================================

class SEOOptimizerEngine:
    """
    Advanced SEO optimization engine for organic discoverability
    Analyzes and optimizes content for search engines and platforms
    """
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'down', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'shall', 'can', 'need',
            'dare', 'ought', 'used', 'it', 'its', 'this', 'that', 'these', 'those'
        }
        
        # SEO best practices
        self.title_length_range = (50, 60)
        self.description_length_range = (150, 160)
        self.ideal_keyword_density = (1.0, 2.5)  # 1-2.5%
        self.ideal_content_length = 1000  # minimum words
        self.heading_levels = ['h1', 'h2', 'h3']
    
    def analyze_keywords(self, content: str, top_n: int = 10) -> List[KeywordData]:
        """
        Analyze keywords in content with density and prominence
        """
        # Clean and tokenize
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        word_freq = Counter(words)
        
        # Remove stop words
        for stop_word in self.stop_words:
            if stop_word in word_freq:
                del word_freq[stop_word]
        
        total_words = len(words)
        keyword_data = []
        
        for word, freq in word_freq.most_common(top_n):
            density = (freq / total_words) * 100 if total_words > 0 else 0
            prominence = self._calculate_prominence(word, content)
            
            # Estimate difficulty and volume (simplified)
            difficulty = min(100, freq * 2)  # Lower frequency = higher difficulty
            volume = freq * 100  # Simplified volume estimation
            
            # Generate related keyword suggestions
            suggestions = self._generate_keyword_suggestions(word)
            
            keyword_data.append(KeywordData(
                keyword=word,
                density=density,
                prominence=prominence,
                difficulty=difficulty,
                volume=volume,
                suggestions=suggestions
            ))
        
        return keyword_data
    
    def _calculate_prominence(self, keyword: str, content: str) -> float:
        """Calculate keyword prominence (position in content)"""
        content_lower = content.lower()
        keyword_lower = keyword.lower()
        
        # Check if in first 100 words
        first_100 = ' '.join(content_lower.split()[:100])
        in_intro = keyword_lower in first_100
        
        # Check if in last 100 words
        last_100 = ' '.join(content_lower.split()[-100:])
        in_conclusion = keyword_lower in last_100
        
        # Check if in headings (simplified)
        in_heading = bool(re.search(rf'^#+\s*{keyword_lower}', content_lower, re.MULTILINE))
        
        prominence = 0.0
        if in_intro:
            prominence += 0.4
        if in_heading:
            prominence += 0.3
        if in_conclusion:
            prominence += 0.3
        
        return prominence
    
    def _generate_keyword_suggestions(self, keyword: str) -> List[str]:
        """Generate related keyword suggestions"""
        # Simple prefix/suffix variations (would use API in production)
        prefixes = ['best', 'top', 'how to', 'guide to', 'ultimate']
        suffixes = ['guide', 'tutorial', 'tips', 'strategies', 'methods']
        
        suggestions = []
        for prefix in prefixes[:2]:
            suggestions.append(f"{prefix} {keyword}")
        for suffix in suffixes[:2]:
            suggestions.append(f"{keyword} {suffix}")
        
        return suggestions
    
    def calculate_seo_score(self, 
                           title: str,
                           description: str,
                           content: str) -> SEOScore:
        """
        Calculate comprehensive SEO score with detailed breakdown
        """
        suggestions = []
        
        # Title score
        title_score = self._score_title(title, suggestions)
        
        # Description score
        description_score = self._score_description(description, suggestions)
        
        # Content score
        content_score = self._score_content(content, suggestions)
        
        # Technical score
        technical_score = self._score_technical_elements(content, suggestions)
        
        # Overall score (weighted average)
        overall_score = (
            title_score * 0.25 +
            description_score * 0.25 +
            content_score * 0.35 +
            technical_score * 0.15
        )
        
        return SEOScore(
            overall_score=overall_score,
            title_score=title_score,
            description_score=description_score,
            content_score=content_score,
            technical_score=technical_score,
            suggestions=suggestions
        )
    
    def _score_title(self, title: str, suggestions: List[str]) -> float:
        """Score title for SEO optimization"""
        score = 0.0
        title_lower = title.lower()
        
        # Length check
        title_len = len(title)
        if self.title_length_range[0] <= title_len <= self.title_length_range[1]:
            score += 30
        elif title_len >= self.title_length_range[0]:
            score += 20
        else:
            suggestions.append("Title is too short. Aim for 50-60 characters.")
        
        # Keywords presence
        if any(word in title_lower for word in ['guide', 'tutorial', 'how', 'best', 'top']):
            score += 20
        
        # Numbers (add specificity)
        if re.search(r'\d+', title):
            score += 10
        
        # Power words
        power_words = ['ultimate', 'complete', 'essential', 'comprehensive', 'definitive']
        if any(word in title_lower for word in power_words):
            score += 20
        
        # No filler words
        if not any(stop_word in title_lower for stop_word in ['amazing', 'awesome', 'great']):
            score += 10
        
        # Question format (curiosity)
        if '?' in title:
            score += 10
        
        return min(score, 100)
    
    def _score_description(self, description: str, suggestions: List[str]) -> float:
        """Score meta description for SEO"""
        score = 0.0
        desc_len = len(description)
        
        # Length check
        if self.description_length_range[0] <= desc_len <= self.description_length_range[1]:
            score += 40
        elif desc_len >= self.description_length_range[0]:
            score += 30
        else:
            suggestions.append("Description is too short. Aim for 150-160 characters.")
        
        # Call to action
        cta_phrases = ['learn more', 'discover', 'find out', 'explore', 'get started']
        if any(phrase in description.lower() for phrase in cta_phrases):
            score += 20
        
        # Keywords
        if len(description.split()) >= 10:  # Has substantial content
            score += 20
        
        # No repetition
        words = description.lower().split()
        if len(set(words)) / len(words) > 0.7:  # Good uniqueness
            score += 20
        
        return min(score, 100)
    
    def _score_content(self, content: str, suggestions: List[str]) -> float:
        """Score main content for SEO"""
        score = 0.0
        word_count = len(content.split())
        
        # Length check
        if word_count >= self.ideal_content_length:
            score += 30
        elif word_count >= 500:
            score += 20
        else:
            suggestions.append(f"Content is too short ({word_count} words). Aim for 1000+ words.")
        
        # Heading structure
        headings = re.findall(r'^#+\s+.+$', content, re.MULTILINE)
        if len(headings) >= 3:
            score += 20
        else:
            suggestions.append("Add more headings to structure your content.")
        
        # Paragraph length (readability)
        paragraphs = content.split('\n\n')
        avg_para_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        if 50 <= avg_para_length <= 150:
            score += 15
        
        # Internal links (placeholder check)
        if 'link' in content.lower() or 'href' in content.lower():
            score += 15
        
        # Image alt text presence
        if 'alt=' in content or 'alt =' in content:
            score += 10
        
        # Keyword density check
        keywords = self.analyze_keywords(content, top_n=5)
        if keywords:
            avg_density = sum(k.density for k in keywords) / len(keywords)
            if self.ideal_keyword_density[0] <= avg_density <= self.ideal_keyword_density[1]:
                score += 10
            else:
                suggestions.append(f"Keyword density is {avg_density:.1f}%. Aim for 1-2.5%.")
        
        return min(score, 100)
    
    def _score_technical_elements(self, content: str, suggestions: List[str]) -> float:
        """Score technical SEO elements"""
        score = 0.0
        
        # URL structure (placeholder)
        suggestions.append("Ensure URL is short, descriptive, and contains keywords.")
        
        # Mobile responsiveness (placeholder)
        score += 25  # Assume responsive by default
        suggestions.append("Ensure content is mobile-responsive.")
        
        # Page speed (placeholder)
        score += 25  # Assume acceptable speed
        suggestions.append("Optimize images and minify CSS/JS for better load times.")
        
        # SSL/HTTPS (placeholder)
        score += 25  # Assume HTTPS
        suggestions.append("Ensure site uses HTTPS.")
        
        # Schema markup
        score += 25
        suggestions.append("Add structured data markup for rich snippets.")
        
        return min(score, 100)
    
    def optimize_title(self, original_title: str, keywords: List[str]) -> str:
        """
        Auto-optimize title for SEO
        """
        title_lower = original_title.lower()
        
        # Add power word if missing
        power_words = ['ultimate', 'complete', 'essential', 'comprehensive']
        if not any(word in title_lower for word in power_words):
            original_title = f"The Ultimate {original_title}"
        
        # Add year if missing
        if not re.search(r'20\d{2}', original_title):
            import datetime
            original_title = f"{original_title} ({datetime.datetime.now().year})"
        
        # Ensure length is optimal
        if len(original_title) < self.title_length_range[0]:
            # Add relevant keyword
            if keywords:
                original_title = f"{original_title}: {keywords[0].title()}"
        
        return original_title
    
    def optimize_description(self, 
                            content: str, 
                            keywords: List[str],
                            target_length: int = 155) -> str:
        """
        Auto-generate optimized meta description
        """
        # Extract key sentences from content
        sentences = content.split('.')
        
        # Prioritize sentences with keywords
        keyword_sentences = []
        other_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if any(keyword.keyword.lower() in sentence.lower() for keyword in keywords):
                keyword_sentences.append(sentence)
            else:
                other_sentences.append(sentence)
        
        # Build description
        description_parts = []
        
        # Start with keyword-rich sentence
        if keyword_sentences:
            description_parts.append(keyword_sentences[0])
        
        # Add informative sentence
        if other_sentences:
            description_parts.append(other_sentences[0])
        
        # Add call to action
        description_parts.append("Learn more and get started today.")
        
        description = ' '.join(description_parts)
        
        # Trim to optimal length
        if len(description) > target_length:
            description = description[:target_length-3] + "..."
        
        return description
    
    def generate_tags(self, keywords: List[str], content: str, max_tags: int = 15) -> List[str]:
        """
        Generate optimized tags from keywords and content
        """
        tags = []
        
        # Add top keywords
        for keyword_data in keywords[:8]:
            tags.append(keyword_data.keyword)
        
        # Add keyword suggestions
        for keyword_data in keywords[:5]:
            tags.extend(keyword_data.suggestions[:2])
        
        # Add category-specific tags (simplified)
        content_lower = content.lower()
        category_tags = []
        if any(word in content_lower for word in ['tutorial', 'guide', 'how to']):
            category_tags.append('tutorial')
        if any(word in content_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
            category_tags.append('artificial intelligence')
        if any(word in content_lower for word in ['automation', 'productivity', 'efficiency']):
            category_tags.append('automation')
        
        tags.extend(category_tags)
        
        # Remove duplicates and limit
        unique_tags = list(set(tag.lower() for tag in tags))
        return unique_tags[:max_tags]
    
    def generate_schema_markup(self, 
                              content_type: str,
                              title: str,
                              description: str,
                              author: str = "ZI Autonomous System") -> str:
        """
        Generate structured data markup for rich snippets
        """
        schema_templates = {
            'article': {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "description": description,
                "author": {
                    "@type": "Person",
                    "name": author
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "ZI Autonomous System",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://takshun-0024-14.web.app/logo.png"
                    }
                }
            },
            'video': {
                "@context": "https://schema.org",
                "@type": "VideoObject",
                "name": title,
                "description": description,
                "author": {
                    "@type": "Person",
                    "name": author
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "ZI Autonomous System"
                }
            },
            'software': {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": title,
                "description": description,
                "author": {
                    "@type": "Person",
                    "name": author
                },
                "applicationCategory": "BusinessApplication"
            }
        }
        
        return json.dumps(schema_templates.get(content_type, schema_templates['article']), indent=2)
    
    def optimize_content(self, 
                         title: str,
                         description: str,
                         content: str,
                         content_type: str = "article") -> OptimizedContent:
        """
        Complete SEO optimization pipeline
        """
        # Analyze keywords
        keywords = self.analyze_keywords(content, top_n=10)
        
        # Optimize title
        optimized_title = self.optimize_title(title, keywords)
        
        # Optimize description
        optimized_description = self.optimize_description(content, keywords)
        
        # Generate tags
        tags = self.generate_tags(keywords, content)
        
        # Generate schema markup
        schema_markup = self.generate_schema_markup(content_type, optimized_title, optimized_description)
        
        # Generate meta tags
        meta_tags = {
            "title": optimized_title,
            "description": optimized_description,
            "keywords": ", ".join([k.keyword for k in keywords[:5]]),
            "og:title": optimized_title,
            "og:description": optimized_description,
            "og:type": content_type,
            "twitter:card": "summary_large_image",
            "twitter:title": optimized_title,
            "twitter:description": optimized_description
        }
        
        # Calculate final SEO score
        seo_score = self.calculate_seo_score(optimized_title, optimized_description, content)
        
        # Generate canonical URL (simplified)
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', optimized_title).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        canonical_url = f"https://takshun-0024-14.web.app/{slug}"
        
        return OptimizedContent(
            title=optimized_title,
            description=optimized_description,
            content=content,
            keywords=[k.keyword for k in keywords],
            tags=tags,
            canonical_url=canonical_url,
            schema_markup=schema_markup,
            meta_tags=meta_tags,
            seo_score=seo_score
        )

# ======================================================================================
# TRENDING TOPIC DISCOVERY
# ======================================================================================

class TrendingTopicDiscovery:
    """
    Discover trending topics for SEO content opportunities
    """
    
    def __init__(self):
        self.trending_keywords = [
            "AI automation", "autonomous agents", "machine learning",
            "productivity hacks", "business automation", "content generation",
            "video AI", "natural language processing", "workflow automation"
        ]
    
    def get_trending_topics(self, limit: int = 10) -> List[str]:
        """Get current trending topics (would use real API in production)"""
        return self.trending_keywords[:limit]
    
    def analyze_topic_opportunity(self, topic: str) -> Dict:
        """Analyze SEO opportunity for a topic"""
        return {
            "topic": topic,
            "difficulty": "medium",
            "volume": "high",
            "competition": "medium",
            "opportunity_score": 75,
            "suggested_keywords": [
                f"best {topic}",
                f"{topic} guide",
                f"how to {topic}",
                f"{topic} tutorial"
            ]
        }

# ======================================================================================
# ENTRY POINT
# ======================================================================================

if __name__ == "__main__":
    import json
    
    logging.basicConfig(level=logging.INFO)
    
    # Test SEO optimizer
    optimizer = SEOOptimizerEngine()
    
    # Sample content
    title = "How to Use AI for Business Automation"
    description = "Learn how artificial intelligence can transform your business processes."
    content = """
    Artificial intelligence is revolutionizing how businesses operate in the modern world.
    From automating repetitive tasks to providing insights through data analysis, AI tools
    are becoming essential for competitive advantage. This guide explores the best AI automation
    strategies for businesses of all sizes.
    
    The integration of AI agents into business workflows can significantly improve efficiency
    and reduce operational costs. Companies that adopt these technologies early are seeing
    substantial improvements in productivity and customer satisfaction.
    """
    
    print("🔍 SEO Analysis")
    keywords = optimizer.analyze_keywords(content)
    print(f"Top keywords: {[k.keyword for k in keywords[:5]]}")
    
    # Calculate SEO score
    seo_score = optimizer.calculate_seo_score(title, description, content)
    print(f"\n📊 SEO Score: {seo_score.overall_score:.1f}/100")
    print(f"  Title: {seo_score.title_score:.1f}/100")
    print(f"  Description: {seo_score.description_score:.1f}/100")
    print(f"  Content: {seo_score.content_score:.1f}/100")
    print(f"  Technical: {seo_score.technical_score:.1f}/100")
    
    print(f"\n💡 Suggestions:")
    for suggestion in seo_score.suggestions[:5]:
        print(f"  - {suggestion}")
    
    # Optimize content
    print("\n🚀 Optimizing content...")
    optimized = optimizer.optimize_content(title, description, content)
    
    print(f"Original Title: {title}")
    print(f"Optimized Title: {optimized.title}")
    print(f"Optimized Description: {optimized.description}")
    print(f"Tags: {', '.join(optimized.tags[:5])}")
    print(f"Canonical URL: {optimized.canonical_url}")
    
    print(f"\n📈 Final SEO Score: {optimized.seo_score.overall_score:.1f}/100")