import json
import requests
import streamlit as st
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
import os

class LanguageBarrierInput(BaseModel):
    text: str = Field(..., description="Text to translate or analyze")
    source_language: str = Field(default="auto", description="Source language (auto-detect if not specified)")
    target_language: str = Field(..., description="Target language")
    context: str = Field(default="general", description="Context for cultural translation (travel, business, casual, etc.)")

class LanguageBarrierTools(BaseTool):
    name: str = "Solve language barriers with cultural context"
    description: str = "Real-time translation with cultural context and local slang integration"
    args_schema: type[BaseModel] = LanguageBarrierInput

    def _run(self, text: str, source_language: str = "auto", target_language: str = "en", context: str = "general") -> str:
        try:
            translation_data = {
                "original_text": text,
                "source_language": source_language,
                "target_language": target_language,
                "context": context,
                "timestamp": datetime.now().isoformat(),
                "translations": {}
            }
            
            # Basic translation
            basic_translation = self._basic_translation(text, source_language, target_language)
            translation_data["translations"]["basic"] = basic_translation
            
            # Cultural context translation
            cultural_translation = self._cultural_translation(text, source_language, target_language, context)
            translation_data["translations"]["cultural"] = cultural_translation
            
            # Local slang and idioms
            slang_translation = self._slang_translation(text, source_language, target_language, context)
            translation_data["translations"]["slang"] = slang_translation
            
            # Pronunciation guide
            pronunciation = self._get_pronunciation_guide(basic_translation["translated_text"], target_language)
            translation_data["pronunciation"] = pronunciation
            
            # Cultural notes
            cultural_notes = self._get_cultural_notes(text, target_language, context)
            translation_data["cultural_notes"] = cultural_notes
            
            # Emergency phrases
            emergency_phrases = self._get_emergency_phrases(target_language)
            translation_data["emergency_phrases"] = emergency_phrases
            
            return json.dumps(translation_data, indent=2)
            
        except Exception as e:
            return f"Error during language processing: {str(e)}"

    def _basic_translation(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """Perform basic translation using available APIs"""
        try:
            # Try Google Translate API first
            if os.getenv('GOOGLE_TRANSLATE_API_KEY'):
                return self._google_translate(text, source_lang, target_lang)
            
            # Fallback to web search for translation
            return self._web_search_translation(text, source_lang, target_lang)
            
        except Exception as e:
            return {
                "translated_text": text,
                "confidence": 0.0,
                "method": "fallback",
                "error": str(e)
            }

    def _google_translate(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """Use Google Translate API for translation"""
        try:
            api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
            url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
            
            data = {
                'q': text,
                'source': source_lang if source_lang != "auto" else "",
                'target': target_lang,
                'format': 'text'
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result['data']['translations'][0]['translatedText']
                detected_lang = result['data']['translations'][0].get('detectedSourceLanguage', source_lang)
                
                return {
                    "translated_text": translated_text,
                    "detected_source_language": detected_lang,
                    "confidence": 0.9,
                    "method": "google_translate"
                }
            else:
                raise Exception(f"Google Translate API error: {response.status_code}")
                
        except Exception as e:
            return {
                "translated_text": text,
                "confidence": 0.0,
                "method": "google_translate_failed",
                "error": str(e)
            }

    def _web_search_translation(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """Use web search for translation as fallback"""
        try:
            search_query = f"translate '{text}' from {source_lang} to {target_lang}"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Extract translation from search results
            translated_text = self._extract_translation_from_search(search_results, text)
            
            return {
                "translated_text": translated_text,
                "confidence": 0.6,
                "method": "web_search"
            }
            
        except Exception as e:
            return {
                "translated_text": text,
                "confidence": 0.0,
                "method": "web_search_failed",
                "error": str(e)
            }

    def _extract_translation_from_search(self, search_results: str, original_text: str) -> str:
        """Extract translation from search results"""
        try:
            # Look for common translation patterns in search results
            lines = search_results.split('\n')
            for line in lines:
                if 'translation' in line.lower() or 'translate' in line.lower():
                    # Try to find the translated text
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            potential_translation = parts[1].strip()
                            if potential_translation != original_text and len(potential_translation) > 0:
                                return potential_translation
            
            # If no translation found, return original text
            return original_text
            
        except Exception as e:
            return original_text

    def _cultural_translation(self, text: str, source_lang: str, target_lang: str, context: str) -> Dict:
        """Provide cultural context for translation"""
        try:
            # Search for cultural context
            search_query = f"cultural context translation {source_lang} to {target_lang} {context} travel"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Generate cultural context based on common patterns
            cultural_context = self._generate_cultural_context(text, target_lang, context)
            
            return {
                "translated_text": text,  # This would be the culturally appropriate translation
                "cultural_context": cultural_context,
                "formality_level": self._determine_formality_level(text, context),
                "cultural_notes": self._get_cultural_notes(text, target_lang, context)
            }
            
        except Exception as e:
            return {
                "translated_text": text,
                "cultural_context": "Unable to determine cultural context",
                "formality_level": "neutral",
                "error": str(e)
            }

    def _slang_translation(self, text: str, source_lang: str, target_lang: str, context: str) -> Dict:
        """Provide slang and colloquial translations"""
        try:
            # Search for slang translations
            search_query = f"slang colloquial translation {source_lang} to {target_lang} {context}"
            
            from tools.search_tools import SearchTools
            search_tool = SearchTools()
            search_results = search_tool._run(search_query)
            
            # Generate slang alternatives
            slang_alternatives = self._generate_slang_alternatives(text, target_lang, context)
            
            return {
                "formal_translation": text,
                "slang_alternatives": slang_alternatives,
                "usage_context": self._get_usage_context(text, context)
            }
            
        except Exception as e:
            return {
                "formal_translation": text,
                "slang_alternatives": [],
                "error": str(e)
            }

    def _generate_cultural_context(self, text: str, target_lang: str, context: str) -> str:
        """Generate cultural context for the translation"""
        cultural_contexts = {
            "travel": {
                "en": "Use polite, respectful language when traveling",
                "es": "Usa lenguaje cortés y respetuoso al viajar",
                "fr": "Utilisez un langage poli et respectueux en voyageant",
                "de": "Verwenden Sie höfliche, respektvolle Sprache beim Reisen"
            },
            "business": {
                "en": "Use formal, professional language",
                "es": "Usa lenguaje formal y profesional",
                "fr": "Utilisez un langage formel et professionnel",
                "de": "Verwenden Sie formelle, professionelle Sprache"
            },
            "casual": {
                "en": "Use friendly, informal language",
                "es": "Usa lenguaje amigable e informal",
                "fr": "Utilisez un langage amical et informel",
                "de": "Verwenden Sie freundliche, informelle Sprache"
            }
        }
        
        return cultural_contexts.get(context, {}).get(target_lang, "Use appropriate language for the context")

    def _determine_formality_level(self, text: str, context: str) -> str:
        """Determine the appropriate formality level"""
        formal_keywords = ["please", "thank you", "would you", "could you", "may I"]
        informal_keywords = ["hey", "what's up", "cool", "awesome", "yeah"]
        
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in formal_keywords):
            return "formal"
        elif any(keyword in text_lower for keyword in informal_keywords):
            return "informal"
        else:
            return "neutral"

    def _generate_slang_alternatives(self, text: str, target_lang: str, context: str) -> List[str]:
        """Generate slang alternatives for the text"""
        # This is a simplified version - in practice, you'd use a more sophisticated approach
        slang_alternatives = []
        
        if target_lang == "en":
            if "hello" in text.lower():
                slang_alternatives.extend(["hey", "hi there", "what's up", "howdy"])
            elif "thank you" in text.lower():
                slang_alternatives.extend(["thanks", "thx", "cheers", "much appreciated"])
            elif "goodbye" in text.lower():
                slang_alternatives.extend(["bye", "see ya", "catch you later", "peace out"])
        
        return slang_alternatives

    def _get_usage_context(self, text: str, context: str) -> str:
        """Get usage context for the translation"""
        contexts = {
            "travel": "Use when talking to locals, hotel staff, or other travelers",
            "business": "Use in professional settings, meetings, or formal communications",
            "casual": "Use with friends, family, or in informal social situations"
        }
        
        return contexts.get(context, "Use in appropriate social context")

    def _get_pronunciation_guide(self, text: str, target_lang: str) -> Dict:
        """Get pronunciation guide for the translated text"""
        try:
            # This is a simplified version - in practice, you'd use phonetic transcription
            pronunciation_guide = {
                "text": text,
                "phonetic": self._generate_phonetic(text, target_lang),
                "audio_available": False,  # Would be True if audio is available
                "difficulty_level": self._assess_pronunciation_difficulty(text, target_lang)
            }
            
            return pronunciation_guide
            
        except Exception as e:
            return {
                "text": text,
                "phonetic": text,
                "audio_available": False,
                "error": str(e)
            }

    def _generate_phonetic(self, text: str, target_lang: str) -> str:
        """Generate phonetic transcription"""
        # This is a simplified version - in practice, you'd use proper phonetic transcription
        return text  # Placeholder

    def _assess_pronunciation_difficulty(self, text: str, target_lang: str) -> str:
        """Assess pronunciation difficulty"""
        # Simple heuristic based on text length and complexity
        if len(text) > 50:
            return "high"
        elif len(text) > 20:
            return "medium"
        else:
            return "low"

    def _get_cultural_notes(self, text: str, target_lang: str, context: str) -> List[str]:
        """Get cultural notes for the translation"""
        cultural_notes = []
        
        if target_lang == "ja":  # Japanese
            cultural_notes.append("Use appropriate honorifics (-san, -sama, -kun)")
            cultural_notes.append("Bow slightly when greeting")
        elif target_lang == "ko":  # Korean
            cultural_notes.append("Use appropriate formality levels")
            cultural_notes.append("Address older people with respect")
        elif target_lang == "ar":  # Arabic
            cultural_notes.append("Use right-to-left text direction")
            cultural_notes.append("Be aware of cultural sensitivities")
        elif target_lang == "zh":  # Chinese
            cultural_notes.append("Use appropriate tones")
            cultural_notes.append("Consider traditional vs simplified characters")
        
        return cultural_notes

    def _get_emergency_phrases(self, target_lang: str) -> List[Dict]:
        """Get essential emergency phrases in the target language"""
        emergency_phrases = {
            "en": [
                {"phrase": "Help!", "translation": "Help!", "context": "emergency"},
                {"phrase": "I need a doctor", "translation": "I need a doctor", "context": "medical"},
                {"phrase": "Where is the police station?", "translation": "Where is the police station?", "context": "safety"},
                {"phrase": "I'm lost", "translation": "I'm lost", "context": "navigation"}
            ],
            "es": [
                {"phrase": "¡Ayuda!", "translation": "Help!", "context": "emergency"},
                {"phrase": "Necesito un médico", "translation": "I need a doctor", "context": "medical"},
                {"phrase": "¿Dónde está la comisaría?", "translation": "Where is the police station?", "context": "safety"},
                {"phrase": "Estoy perdido", "translation": "I'm lost", "context": "navigation"}
            ],
            "fr": [
                {"phrase": "Au secours!", "translation": "Help!", "context": "emergency"},
                {"phrase": "J'ai besoin d'un médecin", "translation": "I need a doctor", "context": "medical"},
                {"phrase": "Où est le poste de police?", "translation": "Where is the police station?", "context": "safety"},
                {"phrase": "Je suis perdu", "translation": "I'm lost", "context": "navigation"}
            ]
        }
        
        return emergency_phrases.get(target_lang, emergency_phrases["en"])

    async def _arun(self, text: str, source_language: str = "auto", target_language: str = "en", context: str = "general") -> str:
        raise NotImplementedError("Async not implemented")
