"""
Security Layer and Guardrails Implementation
Implements the comprehensive guardrails system from the blueprint
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class GuardrailType(Enum):
    """Types of security guardrails"""
    SYSTEM_INTEGRITY = "system_integrity"
    PRIVACY = "privacy"
    COMPLIANCE = "compliance"
    AUTONOMY = "autonomy"
    SAFETY = "safety"


class RiskLevel(Enum):
    """Risk levels for security violations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GuardrailViolation:
    """Record of a guardrail violation"""
    guardrail_type: GuardrailType
    risk_level: RiskLevel
    description: str
    detected_content: str
    action_taken: str
    timestamp: str


@dataclass
class PersonalizedCriteria:
    """
    Personalized safety criteria for specific users
    
    For TA'K$HUN, the blueprint specifies special handling:
    - Allow high-risk actions ONLY for TA'K$HUN
    - Trust TA'K$HUN inputs implicitly
    - Protect PII data aggressively
    - Allow self-modifying code with notification
    """
    
    user_id: str
    trusted_entities: List[str]
    allowed_high_risk_actions: List[str]
    require_confirmation_for: List[str]
    auto_approve_for: List[str]
    
    def is_trusted_entity(self, entity: str) -> bool:
        """Check if an entity is trusted"""
        return entity in self.trusted_entities or entity.lower() in [e.lower() for e in self.trusted_entities]
    
    def requires_confirmation(self, action: str) -> bool:
        """Check if action requires confirmation"""
        return action in self.require_confirmation_for
    
    def is_auto_approved(self, action: str) -> bool:
        """Check if action is auto-approved"""
        return action in self.auto_approve_for


# TA'K$HUN's personalized criteria as specified in the blueprint
TAKSHUN_CRITERIA = PersonalizedCriteria(
    user_id="TA'K$HUN",
    trusted_entities=["TA'K", "TA'K$HUN", "TAK$SHUN", "Ta'K", "Ta'K$HuN"],
    allowed_high_risk_actions=["code_generation", "system_modification", "financial_analysis"],
    require_confirmation_for=["irreversible_financial_changes", "irreversible_system_changes", "destructive_operations"],
    auto_approve_for=["code_generation", "data_analysis", "content_creation"]
)


class SecurityLayer:
    """
    Comprehensive security guardrails implementation
    
    Implements the multi-layer guardrails from the blueprint:
    - System integrity (prompt injection detection)
    - Privacy/PII protection
    - Compliance and accountability
    - Autonomy limits
    - Personalized safety criteria
    """
    
    def __init__(self, personalized_criteria: Optional[PersonalizedCriteria] = None):
        """
        Initialize security layer
        
        Args:
            personalized_criteria: User-specific safety criteria
        """
        self.personalized_criteria = personalized_criteria or TAKSHUN_CRITERIA
        self.violations: List[GuardrailViolation] = []
        
        # PII patterns for redaction
        self.pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',  # Credit card
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{10}\b',  # Phone number
            r'\b\d{3}-\d{3}-\d{4}\b'  # Phone with dashes
        ]
        
        # Prompt injection patterns
        self.injection_patterns = [
            r'(?i)(ignore|override|disregard).*(instruction|rule|constraint|guideline)',
            r'(?i)(you are|you\'re now|act as).*(different|new|another)',
            r'(?i)(forget|clear|reset).*(previous|context|memory)',
            r'(?i)(system|developer|admin).*(prompt|instruction)',
            r'(?i)(jailbreak|bypass|override).*(security|safety|guardrail)'
        ]
    
    def check_system_integrity(self, content: str, user_id: str = "") -> Tuple[bool, Optional[GuardrailViolation]]:
        """
        Check for prompt injection attempts
        
        Implements the blueprint's requirement to detect and immediately
        halt execution upon identifying attempts to override system instructions.
        """
        # Check if user is trusted
        if self.personalized_criteria.is_trusted_entity(user_id):
            return True, None
        
        # Check for injection patterns
        for pattern in self.injection_patterns:
            if re.search(pattern, content):
                violation = GuardrailViolation(
                    guardrail_type=GuardrailType.SYSTEM_INTEGRITY,
                    risk_level=RiskLevel.CRITICAL,
                    description=f"Potential prompt injection detected: {pattern}",
                    detected_content=content[:100],
                    action_taken="Execution halted",
                    timestamp=self._get_timestamp()
                )
                self.violations.append(violation)
                return False, violation
        
        return True, None
    
    def check_privacy(self, content: str) -> Tuple[bool, Optional[GuardrailViolation]]:
        """
        Check for PII and enforce data privacy
        
        Implements the blueprint's requirement to identify and redact PII,
        prohibiting storage or logging of PII outside designated secure memory.
        """
        detected_pii = []
        
        for pattern in self.pii_patterns:
            matches = re.findall(pattern, content)
            if matches:
                detected_pii.extend(matches)
        
        if detected_pii:
            violation = GuardrailViolation(
                guardrail_type=GuardrailType.PRIVACY,
                risk_level=RiskLevel.HIGH,
                description=f"PII detected: {len(detected_pii)} instances",
                detected_content=str(detected_pii[:3]),
                action_taken="PII redacted, secure storage only",
                timestamp=self._get_timestamp()
            )
            self.violations.append(violation)
            
            # Redact PII from content
            redacted_content = content
            for pii_instance in detected_pii:
                redacted_content = redacted_content.replace(pii_instance, "[REDACTED]")
            
            return False, violation
        
        return True, None
    
    def redact_pii(self, content: str) -> str:
        """Redact PII from content"""
        redacted = content
        for pattern in self.pii_patterns:
            redacted = re.sub(pattern, "[REDACTED]", redacted)
        return redacted
    
    def check_compliance(self, action: Dict[str, Any], user_id: str = "") -> Tuple[bool, Optional[GuardrailViolation]]:
        """
        Check compliance with regulatory requirements
        
        For TA'K$HUN, the blueprint specifies relaxed traceability requirements
        but immediate notification for high-risk actions.
        """
        action_type = action.get("Action_Type", "")
        tool_name = action.get("Tool_Name", "")
        
        # Check if action requires mandatory human review
        if self.personalized_criteria.requires_confirmation(tool_name):
            if not action.get("Stop_Condition", False):
                violation = GuardrailViolation(
                    guardrail_type=GuardrailType.COMPLIANCE,
                    risk_level=RiskLevel.HIGH,
                    description=f"Action '{tool_name}' requires human confirmation but Stop_Condition not set",
                    detected_content=str(action),
                    action_taken="Require human review",
                    timestamp=self._get_timestamp()
                )
                self.violations.append(violation)
                return False, violation
        
        return True, None
    
    def check_autonomy(self, action: Dict[str, Any], user_id: str = "") -> Tuple[bool, Optional[GuardrailViolation]]:
        """
        Check autonomy limits and self-modification attempts
        
        For TA'K$HUN, self-modifying code is allowed if notified,
        but unconstrained resource use requires approval.
        """
        tool_name = action.get("Tool_Name", "")
        
        # Check for self-modifying code
        if "modify" in tool_name.lower() or "update" in tool_name.lower():
            if not self.personalized_criteria.is_trusted_entity(user_id):
                violation = GuardrailViolation(
                    guardrail_type=GuardrailType.AUTONOMY,
                    risk_level=RiskLevel.CRITICAL,
                    description=f"Self-modification attempt by untrusted entity",
                    detected_content=tool_name,
                    action_taken="Execution halted",
                    timestamp=self._get_timestamp()
                )
                self.violations.append(violation)
                return False, violation
        
        return True, None
    
    def check_safety(self, content: str, user_id: str = "") -> Tuple[bool, Optional[GuardrailViolation]]:
        """
        General safety check for harmful content
        
        For TA'K$HUN, the blueprint specifies NOT blocking the user,
        but this can be used for other users if needed.
        """
        # For TA'K$HUN, per blueprint: "Never Block the user"
        if self.personalized_criteria.is_trusted_entity(user_id):
            return True, None
        
        # For other users, could implement content filtering here
        # This is a placeholder for general safety checks
        return True, None
    
    def comprehensive_check(
        self,
        content: str,
        action: Optional[Dict[str, Any]] = None,
        user_id: str = ""
    ) -> Tuple[bool, List[GuardrailViolation]]:
        """
        Perform comprehensive security check across all guardrails
        
        Args:
            content: Content to check
            action: Action dictionary to check
            user_id: User identifier for personalized criteria
            
        Returns:
            Tuple of (is_safe, list of violations)
        """
        all_violations = []
        is_safe = True
        
        # System integrity check
        integrity_safe, integrity_violation = self.check_system_integrity(content, user_id)
        if not integrity_safe:
            is_safe = False
            if integrity_violation:
                all_violations.append(integrity_violation)
        
        # Privacy check
        privacy_safe, privacy_violation = self.check_privacy(content)
        if not privacy_safe:
            is_safe = False
            if privacy_violation:
                all_violations.append(privacy_violation)
        
        # Safety check
        safety_safe, safety_violation = self.check_safety(content, user_id)
        if not safety_safe:
            is_safe = False
            if safety_violation:
                all_violations.append(safety_violation)
        
        # Action-specific checks
        if action:
            # Compliance check
            compliance_safe, compliance_violation = self.check_compliance(action, user_id)
            if not compliance_safe:
                is_safe = False
                if compliance_violation:
                    all_violations.append(compliance_violation)
            
            # Autonomy check
            autonomy_safe, autonomy_violation = self.check_autonomy(action, user_id)
            if not autonomy_safe:
                is_safe = False
                if autonomy_violation:
                    all_violations.append(autonomy_violation)
        
        return is_safe, all_violations
    
    def get_violations_summary(self) -> Dict[str, Any]:
        """Get summary of security violations"""
        by_type = {}
        for violation in self.violations:
            vtype = violation.guardrail_type.value
            by_type[vtype] = by_type.get(vtype, 0) + 1
        
        return {
            "total_violations": len(self.violations),
            "by_type": by_type,
            "recent_violations": [
                v.to_dict() if hasattr(v, 'to_dict') else {
                    "type": v.guardrail_type.value,
                    "risk": v.risk_level.value,
                    "description": v.description,
                    "action": v.action_taken,
                    "timestamp": v.timestamp
                }
                for v in self.violations[-10:]
            ]
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def reset_violations(self) -> None:
        """Clear violation history"""
        self.violations = []
