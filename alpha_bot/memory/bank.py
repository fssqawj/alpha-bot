"""Memory Bank - manages collections of memories with different priorities"""

from loguru import logger
import heapq
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from .types import MemoryEntry, MemorySummary, MemoryQuery


class MemoryBank:
    """
    Manages collections of memories with different priorities and handles
    compression when the memory bank grows too large.
    """
    
    def __init__(self, max_entries: int = 6, compression_threshold: int = 6):
        """
        Initialize memory bank
        
        Args:
            max_entries: Maximum number of entries to keep before compression
            compression_threshold: Number of entries that triggers compression
        """
        self.entries: List[MemoryEntry] = []
        self.summaries: List[MemorySummary] = []
        self.max_entries = max_entries
        self.compression_threshold = compression_threshold
        
    def add_entry(self, entry: MemoryEntry):
        """
        Add a memory entry to the bank
        
        Args:
            entry: MemoryEntry to add
        """
        self.entries.append(entry)
        logger.info(f"Added memory entry: {entry}")
        logger.info(f"Memory bank size: {len(self.entries)} entries, threshold: {self.compression_threshold}, max: {self.max_entries}")
        # Check if we need to compress
        if len(self.entries) >= self.compression_threshold:
            self._compress_if_needed()
    
    def _compress_if_needed(self):
        """
        Compress entries if the bank has grown too large
        """
        if len(self.entries) >= self.max_entries:
            # Compress half of the oldest entries
            entries_to_compress = self.entries[:len(self.entries)//2]
            if entries_to_compress:
                # Create a summary of these entries
                summary = self._create_summary(entries_to_compress)
                self.summaries.append(summary)
                
                # Remove the compressed entries
                self.entries = self.entries[len(entries_to_compress):]
    
    def _create_summary(self, entries: List[MemoryEntry]) -> MemorySummary:
        """
        Create a summary from a list of entries
        
        Args:
            entries: List of entries to summarize
            
        Returns:
            MemorySummary containing the compressed information
        """
        # Combine key information from all entries
        content_parts = []
        all_tags = set()
        
        for entry in entries:
            content_parts.append(f"Step {entry.step_number} - {entry.skill_name}: {entry.summary}")
            all_tags.update(entry.tags)
        
        title = f"Summary of {len(entries)} steps ({entries[0].step_number}-{entries[-1].step_number})"
        content = "\n".join(content_parts)
        
        return MemorySummary(
            title=title,
            content=content,
            source_entries=[entry.id for entry in entries],
            tags=list(all_tags)
        )
    
    def get_relevant_memories(self, query: MemoryQuery) -> List[MemoryEntry]:
        """
        Retrieve relevant memories based on query criteria
        
        Args:
            query: MemoryQuery specifying retrieval criteria
            
        Returns:
            List of relevant MemoryEntries
        """
        # Filter entries based on query criteria
        relevant_entries = []
        
        for entry in self.entries:
            if entry.importance < query.min_importance:
                continue
                
            if query.date_from and entry.timestamp < query.date_from:
                continue
                
            if query.date_to and entry.timestamp > query.date_to:
                continue
                
            # Check if entry matches keywords
            matches_keywords = not query.keywords  # If no keywords, match all
            if query.keywords:
                text_to_search = f"{entry.skill_name} {entry.thinking} {entry.command} {entry.result} {entry.summary}".lower()
                for keyword in query.keywords:
                    if keyword.lower() in text_to_search:
                        matches_keywords = True
                        break
            
            # Check if entry matches tags
            matches_tags = not query.tags  # If no tags, match all
            if query.tags:
                for tag in query.tags:
                    if tag in entry.tags:
                        matches_tags = True
                        break
            
            if matches_keywords and matches_tags:
                relevant_entries.append(entry)
        
        # Sort by importance and timestamp (most important and recent first)
        relevant_entries.sort(key=lambda x: (x.importance, x.timestamp.timestamp()), reverse=True)
        
        # Limit results
        return relevant_entries[:query.max_results]
    
    def get_recent_entries(self, count: int = 5) -> List[MemoryEntry]:
        """
        Get the most recent entries
        
        Args:
            count: Number of recent entries to return
            
        Returns:
            List of recent MemoryEntries
        """
        return self.entries[-count:] if len(self.entries) >= count else self.entries[:]
    
    def get_summaries(self) -> List[MemorySummary]:
        """
        Get all memory summaries
        
        Returns:
            List of MemorySummaries
        """
        return self.summaries[:]
    
    def get_all_memories(self) -> List[MemoryEntry]:
        """
        Get all memory entries (both compressed and uncompressed)
        
        Returns:
            List of all MemoryEntries
        """
        return self.entries[:]
    
    def clear(self):
        """
        Clear all memories and summaries
        """
        self.entries.clear()
        self.summaries.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the memory bank
        
        Returns:
            Dictionary with memory bank statistics
        """
        return {
            "entry_count": len(self.entries),
            "summary_count": len(self.summaries),
            "total_count": len(self.entries) + len(self.summaries),
            "compression_ratio": len(self.summaries) / max(1, len(self.entries)) if self.entries else 0
        }