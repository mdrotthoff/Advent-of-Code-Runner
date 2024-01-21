"""Advent of Code Runner puzzle model"""

# System libraries
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AnswerResult(Enum):
    """Define the supplied response from the Advent of Code server
    as to the status pf the submitted answer"""
    too_low: int = -1
    correct: int = 0
    too_high: int = 1


@dataclass(frozen=True)
class PuzzleSubmission:
    """Defines the data & results retained about an answer submitted to
    and Advent of Code puzzle part"""
    answer: str
    submitted: datetime
    result: AnswerResult
    server_response: str


@dataclass
class PuzzlePartAnswer:
    """Define the data associated with every submission for a puzzle part"""
    puzzle_part: int
    low_value: str
    high_value: str
    answer: str | None
    submissions: list[PuzzleSubmission]


@dataclass
class PuzzleAnswer:
    year: int
    day: int
    part_1: PuzzlePartAnswer
    part_2: PuzzlePartAnswer


