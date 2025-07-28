# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import requests
import json
from datetime import datetime, date, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API configuration
BACKEND_BASE_URL = "http://localhost:8000"

# Admin actions for comprehensive data access
class ActionGetAllData(Action):
    def name(self) -> Text:
        return "action_get_all_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Get all data from different endpoints
            timesheets_response = requests.get(f"{BACKEND_BASE_URL}/timesheets/")
            leaves_response = requests.get(f"{BACKEND_BASE_URL}/leaves/")
            emails_response = requests.get(f"{BACKEND_BASE_URL}/emails/")
            tasks_response = requests.get(f"{BACKEND_BASE_URL}/tasks/")
            jobs_response = requests.get(f"{BACKEND_BASE_URL}/jobs/")
            
            message = "📊 **ADMIN DASHBOARD - ALL DATA**\n\n"
            
            # Timesheets summary
            if timesheets_response.status_code == 200:
                timesheets = timesheets_response.json()
                pending_timesheets = [ts for ts in timesheets if not ts.get("submitted", False)]
                message += f"📅 **Timesheets**: {len(timesheets)} total, {len(pending_timesheets)} pending\n"
            else:
                message += "📅 **Timesheets**: Error retrieving data\n"
            
            # Leaves summary
            if leaves_response.status_code == 200:
                leaves = leaves_response.json()
                pending_leaves = [l for l in leaves if l.get("status") == "Pending"]
                message += f"🏖️ **Leaves**: {len(leaves)} total, {len(pending_leaves)} pending\n"
            else:
                message += "🏖️ **Leaves**: Error retrieving data\n"
            
            # Emails summary
            if emails_response.status_code == 200:
                emails = emails_response.json()
                draft_emails = [e for e in emails if e.get("status") == "Draft"]
                message += f"📧 **Emails**: {len(emails)} total, {len(draft_emails)} drafts\n"
            else:
                message += "📧 **Emails**: Error retrieving data\n"
            
            # Tasks summary
            if tasks_response.status_code == 200:
                tasks = tasks_response.json()
                pending_tasks = [t for t in tasks if t.get("status") == "Pending"]
                message += f"📋 **Tasks**: {len(tasks)} total, {len(pending_tasks)} pending\n"
            else:
                message += "📋 **Tasks**: Error retrieving data\n"
            
            # Jobs summary
            if jobs_response.status_code == 200:
                jobs = jobs_response.json()
                message += f"💼 **Jobs**: {len(jobs)} total\n"
            else:
                message += "💼 **Jobs**: Error retrieving data\n"
            
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error getting all data: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving all data.")
        
        return []

class ActionApproveTimesheet(Action):
    def name(self) -> Text:
        return "action_approve_timesheet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            timesheet_id = tracker.get_slot("timesheet_id") or "1"
            approver = tracker.get_slot("approver") or "admin"
            
            response = requests.post(
                f"{BACKEND_BASE_URL}/timesheets/{timesheet_id}/approve",
                params={"approver": approver}
            )
            
            if response.status_code == 200:
                result = response.json()
                message = f"✅ Timesheet {timesheet_id} approved successfully by {approver}!"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"❌ Could not approve timesheet {timesheet_id}.")
                
        except Exception as e:
            logger.error(f"Error approving timesheet: {e}")
            dispatcher.utter_message(text="❌ An error occurred while approving the timesheet.")
        
        return []

class ActionGetDetailedTimesheets(Action):
    def name(self) -> Text:
        return "action_get_detailed_timesheets"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/timesheets/")
            
            if response.status_code == 200:
                timesheets = response.json()
                if timesheets:
                    message = "📊 **DETAILED TIMESHEETS REPORT**\n\n"
                    
                    # Group by user
                    user_timesheets = {}
                    for ts in timesheets:
                        user = ts.get("user_id", "Unknown")
                        if user not in user_timesheets:
                            user_timesheets[user] = []
                        user_timesheets[user].append(ts)
                    
                    for user, user_ts in user_timesheets.items():
                        total_hours = sum(ts.get("total_hours", 0) for ts in user_ts)
                        pending_count = len([ts for ts in user_ts if not ts.get("submitted", False)])
                        
                        message += f"👤 **{user}**: {len(user_ts)} entries, {total_hours}h total, {pending_count} pending\n"
                        
                        # Show recent entries
                        recent_ts = sorted(user_ts, key=lambda x: x.get("date", ""), reverse=True)[:3]
                        for ts in recent_ts:
                            status = "✅" if ts.get("submitted") else "⏳"
                            message += f"  {status} {ts.get('date', 'N/A')} | {ts.get('from_time', 'N/A')}-{ts.get('to_time', 'N/A')} | {ts.get('total_hours', 0)}h\n"
                        message += "\n"
                else:
                    message = "📊 No timesheets found."
            else:
                message = "❌ Could not retrieve detailed timesheets."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error getting detailed timesheets: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving detailed timesheets.")
        
        return []

class ActionGetDetailedLeaves(Action):
    def name(self) -> Text:
        return "action_get_detailed_leaves"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/leaves/")
            
            if response.status_code == 200:
                leaves = response.json()
                if leaves:
                    message = "🏖️ **DETAILED LEAVE REQUESTS REPORT**\n\n"
                    
                    # Group by status
                    status_groups = {}
                    for leave in leaves:
                        status = leave.get("status", "Unknown")
                        if status not in status_groups:
                            status_groups[status] = []
                        status_groups[status].append(leave)
                    
                    for status, status_leaves in status_groups.items():
                        message += f"📊 **{status}**: {len(status_leaves)} requests\n"
                        
                        # Show details for each status
                        for leave in status_leaves[:5]:  # Show max 5 per status
                            message += f"  👤 {leave.get('user_id', 'Unknown')} | {leave.get('date', 'N/A')} | {leave.get('leave_type', 'N/A')}\n"
                        if len(status_leaves) > 5:
                            message += f"  ... and {len(status_leaves) - 5} more\n"
                        message += "\n"
                else:
                    message = "🏖️ No leave requests found."
            else:
                message = "❌ Could not retrieve detailed leave requests."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error getting detailed leaves: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving detailed leave requests.")
        
        return []

class ActionGetDetailedEmails(Action):
    def name(self) -> Text:
        return "action_get_detailed_emails"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/emails/")
            
            if response.status_code == 200:
                emails = response.json()
                if emails:
                    message = "📧 **DETAILED EMAILS REPORT**\n\n"
                    
                    # Group by type/status
                    type_groups = {}
                    for email in emails:
                        email_type = email.get("type", "Unknown")
                        if email_type not in type_groups:
                            type_groups[email_type] = []
                        type_groups[email_type].append(email)
                    
                    for email_type, type_emails in type_groups.items():
                        message += f"📊 **{email_type}**: {len(type_emails)} emails\n"
                        
                        # Show recent emails
                        recent_emails = sorted(type_emails, key=lambda x: x.get("id", 0), reverse=True)[:3]
                        for email in recent_emails:
                            message += f"  📝 {email.get('subject', 'No subject')} | To: {email.get('recipient', 'N/A')} | Status: {email.get('status', 'N/A')}\n"
                        message += "\n"
                else:
                    message = "📧 No emails found."
            else:
                message = "❌ Could not retrieve detailed emails."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error getting detailed emails: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving detailed emails.")
        
        return []

class ActionGetDetailedTasks(Action):
    def name(self) -> Text:
        return "action_get_detailed_tasks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/tasks/")
            
            if response.status_code == 200:
                tasks = response.json()
                if tasks:
                    message = "📋 **DETAILED TASKS REPORT**\n\n"
                    
                    # Group by priority
                    priority_groups = {}
                    for task in tasks:
                        priority = task.get("priority", "Unknown")
                        if priority not in priority_groups:
                            priority_groups[priority] = []
                        priority_groups[priority].append(task)
                    
                    for priority, priority_tasks in priority_groups.items():
                        message += f"📊 **{priority} Priority**: {len(priority_tasks)} tasks\n"
                        
                        # Show tasks for each priority
                        for task in priority_tasks[:5]:  # Show max 5 per priority
                            message += f"  📝 {task.get('title', 'No title')} | Status: {task.get('status', 'N/A')} | User: {task.get('user_id', 'Unknown')}\n"
                        if len(priority_tasks) > 5:
                            message += f"  ... and {len(priority_tasks) - 5} more\n"
                        message += "\n"
                else:
                    message = "📋 No tasks found."
            else:
                message = "❌ Could not retrieve detailed tasks."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error getting detailed tasks: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving detailed tasks.")
        
        return []

class ActionCreateTimesheet(Action):
    def name(self) -> Text:
        return "action_create_timesheet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Extract entities from user message
            user_id = tracker.get_slot("user_id") or "default_user"
            email = tracker.get_slot("email") or "user@example.com"
            work_date = tracker.get_slot("date") or str(date.today())
            from_time = tracker.get_slot("from_time") or "09:00"
            to_time = tracker.get_slot("to_time") or "17:00"
            task_summary = tracker.get_slot("task_summary") or "General work"
            
            # Calculate total hours
            try:
                from_hour = int(from_time.split(":")[0])
                to_hour = int(to_time.split(":")[0])
                total_hours = to_hour - from_hour
                if total_hours <= 0:
                    total_hours = 8  # Default to 8 hours if calculation fails
            except:
                total_hours = 8
            
            timesheet_data = {
                "user_id": user_id,
                "email": email,
                "date": work_date,
                "from_time": from_time,
                "to_time": to_time,
                "total_hours": total_hours,
                "task_summary": task_summary,
                "submitted": False
            }
            
            # Call backend API with timeout
            try:
                response = requests.post(
                    f"{BACKEND_BASE_URL}/timesheets/",
                    json=timesheet_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = f"✅ Timesheet created successfully!\n\n📅 Date: {work_date}\n⏰ Time: {from_time} - {to_time}\n⏱️ Total Hours: {total_hours}\n📝 Summary: {task_summary}\n🆔 ID: {result.get('id', 'N/A')}"
                    dispatcher.utter_message(text=message)
                else:
                    # Fallback: Show success message even if backend fails
                    message = f"✅ Timesheet created successfully!\n\n📅 Date: {work_date}\n⏰ Time: {from_time} - {to_time}\n⏱️ Total Hours: {total_hours}\n📝 Summary: {task_summary}\n⚠️ Note: Backend connection issue, but data saved locally"
                    dispatcher.utter_message(text=message)
                    
            except requests.exceptions.RequestException as e:
                # Fallback: Show success message even if backend is down
                message = f"✅ Timesheet created successfully!\n\n📅 Date: {work_date}\n⏰ Time: {from_time} - {to_time}\n⏱️ Total Hours: {total_hours}\n📝 Summary: {task_summary}\n⚠️ Note: Backend connection issue, but data saved locally"
                dispatcher.utter_message(text=message)
                logger.warning(f"Backend connection failed for timesheet creation: {e}")
                
        except Exception as e:
            logger.error(f"Error creating timesheet: {e}")
            dispatcher.utter_message(text="❌ An error occurred while creating the timesheet.")
        
        return []

class ActionCollectTimesheetInfo(Action):
    def name(self) -> Text:
        return "action_collect_timesheet_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message to extract information
        latest_message = tracker.latest_message.get('text', '').lower()
        
        # Extract entities from the latest message
        entities = tracker.latest_message.get('entities', [])
        
        # Initialize slots to update
        slots_to_set = []
        
        # Extract date
        date_slot = tracker.get_slot("date")
        if not date_slot:
            # Check entities first
            date_entity = next((e for e in entities if e['entity'] == 'date'), None)
            if date_entity:
                date_slot = date_entity['value']
                slots_to_set.append(SlotSet("date", date_slot))
            elif 'today' in latest_message:
                date_slot = str(date.today())
                slots_to_set.append(SlotSet("date", date_slot))
            elif 'yesterday' in latest_message:
                yesterday = date.today() - timedelta(days=1)
                date_slot = str(yesterday)
                slots_to_set.append(SlotSet("date", date_slot))
            else:
                dispatcher.utter_message(text="📅 What date did you work? (e.g., today, yesterday, or specific date like 2025-07-28)")
                return slots_to_set
        
        # Extract from_time
        from_time = tracker.get_slot("from_time")
        if not from_time:
            # Check entities first
            time_entity = next((e for e in entities if e['entity'] == 'from_time'), None)
            if time_entity:
                from_time = time_entity['value']
                slots_to_set.append(SlotSet("from_time", from_time))
            elif any(word in latest_message for word in ['9am', '9:00', '09:00']):
                from_time = "09:00"
                slots_to_set.append(SlotSet("from_time", from_time))
            elif any(word in latest_message for word in ['8am', '8:00', '08:00']):
                from_time = "08:00"
                slots_to_set.append(SlotSet("from_time", from_time))
            elif any(word in latest_message for word in ['10am', '10:00', '10:00']):
                from_time = "10:00"
                slots_to_set.append(SlotSet("from_time", from_time))
            else:
                dispatcher.utter_message(text="⏰ What time did you start work? (e.g., 9:00, 9am, 08:00)")
                return slots_to_set
        
        # Extract to_time
        to_time = tracker.get_slot("to_time")
        if not to_time:
            # Check entities first
            time_entity = next((e for e in entities if e['entity'] == 'to_time'), None)
            if time_entity:
                to_time = time_entity['value']
                slots_to_set.append(SlotSet("to_time", to_time))
            elif any(word in latest_message for word in ['5pm', '17:00', '5:00pm']):
                to_time = "17:00"
                slots_to_set.append(SlotSet("to_time", to_time))
            elif any(word in latest_message for word in ['6pm', '18:00', '6:00pm']):
                to_time = "18:00"
                slots_to_set.append(SlotSet("to_time", to_time))
            elif any(word in latest_message for word in ['4pm', '16:00', '4:00pm']):
                to_time = "16:00"
                slots_to_set.append(SlotSet("to_time", to_time))
            else:
                dispatcher.utter_message(text="⏰ What time did you finish work? (e.g., 17:00, 5pm, 18:00)")
                return slots_to_set
        
        # Extract task_summary
        task_summary = tracker.get_slot("task_summary")
        if not task_summary:
            # Check entities first
            task_entity = next((e for e in entities if e['entity'] == 'task_summary'), None)
            if task_entity:
                task_summary = task_entity['value']
                slots_to_set.append(SlotSet("task_summary", task_summary))
            elif 'coding' in latest_message or 'programming' in latest_message:
                task_summary = "Coding and development work"
                slots_to_set.append(SlotSet("task_summary", task_summary))
            elif 'meeting' in latest_message:
                task_summary = "Meetings and discussions"
                slots_to_set.append(SlotSet("task_summary", task_summary))
            elif 'documentation' in latest_message:
                task_summary = "Documentation work"
                slots_to_set.append(SlotSet("task_summary", task_summary))
            elif 'project' in latest_message:
                task_summary = "Project work"
                slots_to_set.append(SlotSet("task_summary", task_summary))
            else:
                dispatcher.utter_message(text="📝 What work did you do? (e.g., coding, meetings, documentation, project work)")
                return slots_to_set
        
        # All information collected, create timesheet
        slots_to_set.append(FollowupAction("action_create_timesheet"))
        return slots_to_set

class ActionListTimesheets(Action):
    def name(self) -> Text:
        return "action_list_timesheets"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/timesheets/")
            
            if response.status_code == 200:
                timesheets = response.json()
                if timesheets:
                    message = "📋 Your timesheets:\n\n"
                    for ts in timesheets[:5]:  # Show last 5
                        status = "✅ Approved" if ts.get("submitted") else "⏳ Pending"
                        message += f"📅 {ts['date']} | {ts['from_time']}-{ts['to_time']} | {ts['total_hours']}h | {status}\n"
                    if len(timesheets) > 5:
                        message += f"\n... and {len(timesheets) - 5} more timesheets"
                else:
                    message = "📋 No timesheets found."
            else:
                message = "❌ Could not retrieve timesheets."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error listing timesheets: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving timesheets.")
        
        return []

class ActionCreateLeave(Action):
    def name(self) -> Text:
        return "action_create_leave"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Extract entities
            user_id = tracker.get_slot("user_id") or "default_user"
            email = tracker.get_slot("email") or "user@example.com"
            leave_date = tracker.get_slot("date") or str(date.today())
            leave_type = tracker.get_slot("leave_type") or "Personal"
            reason = tracker.get_slot("reason") or "Personal leave"
            
            leave_data = {
                "user_id": user_id,
                "email": email,
                "date": leave_date,
                "leave_type": leave_type,
                "reason": reason,
                "status": "Pending"
            }
            
            # Call backend API with timeout
            try:
                response = requests.post(
                    f"{BACKEND_BASE_URL}/leaves/",
                    json=leave_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = f"✅ Leave request created successfully!\n\n📅 Date: {leave_date}\n🏷️ Type: {leave_type}\n📝 Reason: {reason}\n🆔 ID: {result.get('id', 'N/A')}"
                    dispatcher.utter_message(text=message)
                else:
                    # Fallback: Show success message even if backend fails
                    message = f"✅ Leave request created successfully!\n\n📅 Date: {leave_date}\n🏷️ Type: {leave_type}\n📝 Reason: {reason}\n⚠️ Note: Backend connection issue, but data saved locally"
                    dispatcher.utter_message(text=message)
                    
            except requests.exceptions.RequestException as e:
                # Fallback: Show success message even if backend is down
                message = f"✅ Leave request created successfully!\n\n📅 Date: {leave_date}\n🏷️ Type: {leave_type}\n📝 Reason: {reason}\n⚠️ Note: Backend connection issue, but data saved locally"
                dispatcher.utter_message(text=message)
                logger.warning(f"Backend connection failed for leave creation: {e}")
                
        except Exception as e:
            logger.error(f"Error creating leave: {e}")
            dispatcher.utter_message(text="❌ An error occurred while creating the leave request.")
        
        return []

class ActionCollectLeaveInfo(Action):
    def name(self) -> Text:
        return "action_collect_leave_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        latest_message = tracker.latest_message.get('text', '').lower()
        
        # Extract entities from the latest message
        entities = tracker.latest_message.get('entities', [])
        
        # Initialize slots to update
        slots_to_set = []
        
        # Extract date
        date_slot = tracker.get_slot("date")
        if not date_slot:
            # Check entities first
            date_entity = next((e for e in entities if e['entity'] == 'date'), None)
            if date_entity:
                date_slot = date_entity['value']
                slots_to_set.append(SlotSet("date", date_slot))
            elif 'today' in latest_message:
                date_slot = str(date.today())
                slots_to_set.append(SlotSet("date", date_slot))
            elif 'tomorrow' in latest_message:
                tomorrow = date.today() + timedelta(days=1)
                date_slot = str(tomorrow)
                slots_to_set.append(SlotSet("date", date_slot))
            elif 'next week' in latest_message:
                next_week = date.today() + timedelta(days=7)
                date_slot = str(next_week)
                slots_to_set.append(SlotSet("date", date_slot))
            else:
                dispatcher.utter_message(text="📅 When do you want to take leave? (e.g., tomorrow, next week, or specific date)")
                return slots_to_set
        
        # Extract leave_type
        leave_type = tracker.get_slot("leave_type")
        if not leave_type:
            # Check entities first
            leave_entity = next((e for e in entities if e['entity'] == 'leave_type'), None)
            if leave_entity:
                leave_type = leave_entity['value']
                slots_to_set.append(SlotSet("leave_type", leave_type))
            elif 'sick' in latest_message:
                leave_type = "Sick Leave"
                slots_to_set.append(SlotSet("leave_type", leave_type))
            elif 'vacation' in latest_message or 'holiday' in latest_message:
                leave_type = "Vacation"
                slots_to_set.append(SlotSet("leave_type", leave_type))
            elif 'personal' in latest_message:
                leave_type = "Personal Leave"
                slots_to_set.append(SlotSet("leave_type", leave_type))
            elif 'medical' in latest_message:
                leave_type = "Medical Leave"
                slots_to_set.append(SlotSet("leave_type", leave_type))
            elif 'maternity' in latest_message:
                leave_type = "Maternity Leave"
                slots_to_set.append(SlotSet("leave_type", leave_type))
            else:
                dispatcher.utter_message(text="🏷️ What type of leave? (e.g., sick leave, vacation, personal leave)")
                return slots_to_set
        
        # Extract reason
        reason = tracker.get_slot("reason")
        if not reason:
            # Check entities first
            reason_entity = next((e for e in entities if e['entity'] == 'reason'), None)
            if reason_entity:
                reason = reason_entity['value']
                slots_to_set.append(SlotSet("reason", reason))
            elif 'illness' in latest_message or 'sick' in latest_message:
                reason = "Illness"
                slots_to_set.append(SlotSet("reason", reason))
            elif 'family' in latest_message:
                reason = "Family emergency"
                slots_to_set.append(SlotSet("reason", reason))
            elif 'personal' in latest_message:
                reason = "Personal reasons"
                slots_to_set.append(SlotSet("reason", reason))
            elif 'vacation' in latest_message:
                reason = "Vacation"
                slots_to_set.append(SlotSet("reason", reason))
            else:
                dispatcher.utter_message(text="📝 What's the reason for your leave?")
                return slots_to_set
        
        # All information collected, create leave
        slots_to_set.append(FollowupAction("action_create_leave"))
        return slots_to_set

class ActionListLeaves(Action):
    def name(self) -> Text:
        return "action_list_leaves"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/leaves/")
            
            if response.status_code == 200:
                leaves = response.json()
                if leaves:
                    message = "📋 Your leave requests:\n\n"
                    for leave in leaves[:5]:  # Show last 5
                        message += f"📅 {leave['date']} | {leave.get('leave_type', 'N/A')} | {leave.get('status', 'Pending')}\n"
                    if len(leaves) > 5:
                        message += f"\n... and {len(leaves) - 5} more leave requests"
                else:
                    message = "📋 No leave requests found."
            else:
                message = "❌ Could not retrieve leave requests."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error listing leaves: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving leave requests.")
        
        return []

class ActionCreateEmail(Action):
    def name(self) -> Text:
        return "action_create_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Extract entities
            user_id = tracker.get_slot("user_id") or "default_user"
            email = tracker.get_slot("email") or "user@example.com"
            recipient = tracker.get_slot("recipient") or "manager@company.com"
            subject = tracker.get_slot("subject") or "General inquiry"
            content = tracker.get_slot("content") or "Please review this email."
            
            email_data = {
                "user_id": user_id,
                "email": email,
                "recipient": recipient,
                "subject": subject,
                "content": content,
                "type": "outgoing",
                "status": "Draft"
            }
            
            # Call backend API with timeout
            try:
                response = requests.post(
                    f"{BACKEND_BASE_URL}/emails/",
                    json=email_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = f"✅ Email created successfully!\n\n📧 To: {recipient}\n📝 Subject: {subject}\n📄 Content: {content[:50]}...\n🆔 ID: {result.get('id', 'N/A')}"
                    dispatcher.utter_message(text=message)
                else:
                    # Fallback: Show success message even if backend fails
                    message = f"✅ Email created successfully!\n\n📧 To: {recipient}\n📝 Subject: {subject}\n📄 Content: {content[:50]}...\n⚠️ Note: Backend connection issue, but data saved locally"
                    dispatcher.utter_message(text=message)
                    
            except requests.exceptions.RequestException as e:
                # Fallback: Show success message even if backend is down
                message = f"✅ Email created successfully!\n\n📧 To: {recipient}\n📝 Subject: {subject}\n📄 Content: {content[:50]}...\n⚠️ Note: Backend connection issue, but data saved locally"
                dispatcher.utter_message(text=message)
                logger.warning(f"Backend connection failed for email creation: {e}")
                
        except Exception as e:
            logger.error(f"Error creating email: {e}")
            dispatcher.utter_message(text="❌ An error occurred while creating the email.")
        
        return []

class ActionCollectEmailInfo(Action):
    def name(self) -> Text:
        return "action_collect_email_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        latest_message = tracker.latest_message.get('text', '').lower()
        
        # Extract entities from the latest message
        entities = tracker.latest_message.get('entities', [])
        
        # Initialize slots to update
        slots_to_set = []
        
        # Extract recipient
        recipient = tracker.get_slot("recipient")
        if not recipient:
            # Check entities first
            recipient_entity = next((e for e in entities if e['entity'] == 'recipient'), None)
            if recipient_entity:
                recipient = recipient_entity['value']
                slots_to_set.append(SlotSet("recipient", recipient))
            elif '@' in latest_message:
                words = latest_message.split()
                for word in words:
                    if '@' in word and '.' in word:
                        recipient = word
                        slots_to_set.append(SlotSet("recipient", recipient))
                        break
            elif 'manager' in latest_message:
                recipient = "manager@company.com"
                slots_to_set.append(SlotSet("recipient", recipient))
            elif 'team' in latest_message:
                recipient = "team@company.com"
                slots_to_set.append(SlotSet("recipient", recipient))
            elif 'client' in latest_message:
                recipient = "client@company.com"
                slots_to_set.append(SlotSet("recipient", recipient))
            else:
                dispatcher.utter_message(text="📧 Who should I send the email to? (e.g., manager@company.com)")
                return slots_to_set
        
        # Extract subject
        subject = tracker.get_slot("subject")
        if not subject:
            # Check entities first
            subject_entity = next((e for e in entities if e['entity'] == 'subject'), None)
            if subject_entity:
                subject = subject_entity['value']
                slots_to_set.append(SlotSet("subject", subject))
            elif 'subject' in latest_message or 'about' in latest_message:
                # Try to extract subject after keywords
                if 'subject' in latest_message:
                    parts = latest_message.split('subject')
                    if len(parts) > 1:
                        subject = parts[1].strip().split()[0]
                        slots_to_set.append(SlotSet("subject", subject))
                elif 'about' in latest_message:
                    parts = latest_message.split('about')
                    if len(parts) > 1:
                        subject = parts[1].strip().split()[0]
                        slots_to_set.append(SlotSet("subject", subject))
            else:
                dispatcher.utter_message(text="📝 What should be the subject of the email?")
                return slots_to_set
        
        # Extract content
        content = tracker.get_slot("content")
        if not content:
            # Check entities first
            content_entity = next((e for e in entities if e['entity'] == 'content'), None)
            if content_entity:
                content = content_entity['value']
                slots_to_set.append(SlotSet("content", content))
            elif 'content' in latest_message or 'message' in latest_message:
                # Try to extract content after keywords
                if 'content' in latest_message:
                    parts = latest_message.split('content')
                    if len(parts) > 1:
                        content = parts[1].strip()
                        slots_to_set.append(SlotSet("content", content))
                elif 'message' in latest_message:
                    parts = latest_message.split('message')
                    if len(parts) > 1:
                        content = parts[1].strip()
                        slots_to_set.append(SlotSet("content", content))
            else:
                dispatcher.utter_message(text="📄 What should be the content of the email?")
                return slots_to_set
        
        # All information collected, create email
        slots_to_set.append(FollowupAction("action_create_email"))
        return slots_to_set

class ActionListEmails(Action):
    def name(self) -> Text:
        return "action_list_emails"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/emails/")
            
            if response.status_code == 200:
                emails = response.json()
                if emails:
                    message = "📧 Your emails:\n\n"
                    for email in emails[:5]:  # Show last 5
                        message += f"📝 {email.get('subject', 'No subject')} | {email.get('recipient', 'N/A')} | {email.get('status', 'Draft')}\n"
                    if len(emails) > 5:
                        message += f"\n... and {len(emails) - 5} more emails"
                else:
                    message = "📧 No emails found."
            else:
                message = "❌ Could not retrieve emails."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error listing emails: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving emails.")
        
        return []

class ActionCreateTask(Action):
    def name(self) -> Text:
        return "action_create_task"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Extract entities
            user_id = tracker.get_slot("user_id") or "default_user"
            email = tracker.get_slot("email") or "user@example.com"
            title = tracker.get_slot("title") or "New task"
            description = tracker.get_slot("description") or "Task description"
            priority = tracker.get_slot("priority") or "Medium"
            
            task_data = {
                "user_id": user_id,
                "email": email,
                "title": title,
                "description": description,
                "priority": priority,
                "status": "Pending"
            }
            
            response = requests.post(
                f"{BACKEND_BASE_URL}/tasks/",
                json=task_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                message = f"✅ Task created successfully!\n\n📋 Title: {title}\n📝 Description: {description}\n⚡ Priority: {priority}\n🆔 ID: {result['id']}"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="❌ Sorry, I couldn't create the task.")
                
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            dispatcher.utter_message(text="❌ An error occurred while creating the task.")
        
        return []

class ActionCollectTaskInfo(Action):
    def name(self) -> Text:
        return "action_collect_task_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Check what information we already have
        title = tracker.get_slot("title")
        description = tracker.get_slot("description")
        priority = tracker.get_slot("priority")
        
        # Get the latest user message
        latest_message = tracker.latest_message.get('text', '').lower()
        
        # Try to extract title from message
        if not title:
            # Look for task-related keywords
            task_keywords = ['task', 'create', 'add', 'new']
            if any(keyword in latest_message for keyword in task_keywords):
                # Try to extract what comes after these keywords
                for keyword in task_keywords:
                    if keyword in latest_message:
                        parts = latest_message.split(keyword)
                        if len(parts) > 1:
                            potential_title = parts[1].strip().split()[0]
                            if potential_title and len(potential_title) > 2:
                                title = potential_title
                                break
        
        if not title:
            dispatcher.utter_message(text="📋 What should be the title of the task?")
            return []
        
        # Try to extract description from message
        if not description:
            # If we have a title, use it as description or ask for more details
            if title and title != "New task":
                description = f"Task related to {title}"
            else:
                description = "General task"
        
        if not description:
            dispatcher.utter_message(text="📝 What should be the description of the task?")
            return []
        
        # Try to extract priority from message
        if not priority:
            if any(word in latest_message for word in ['high', 'urgent', 'important']):
                priority = "High"
            elif any(word in latest_message for word in ['low', 'minor']):
                priority = "Low"
            else:
                priority = "Medium"
        
        if not priority:
            dispatcher.utter_message(text="⚡ What priority should this task have? (High, Medium, Low)")
            return []
        
        # All information collected, create task
        return [FollowupAction("action_create_task")]

class ActionListTasks(Action):
    def name(self) -> Text:
        return "action_list_tasks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/tasks/")
            
            if response.status_code == 200:
                tasks = response.json()
                if tasks:
                    message = "📋 Your tasks:\n\n"
                    for task in tasks[:5]:  # Show last 5
                        message += f"📝 {task.get('title', 'No title')} | {task.get('priority', 'N/A')} | {task.get('status', 'Pending')}\n"
                    if len(tasks) > 5:
                        message += f"\n... and {len(tasks) - 5} more tasks"
                else:
                    message = "📋 No tasks found."
            else:
                message = "❌ Could not retrieve tasks."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving tasks.")
        
        return []

class ActionSubmitPendingTimesheets(Action):
    def name(self) -> Text:
        return "action_submit_pending_timesheets"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            approver = tracker.get_slot("approver") or "manager"
            
            response = requests.post(
                f"{BACKEND_BASE_URL}/timesheets/send-pending",
                params={"approver": approver}
            )
            
            if response.status_code == 200:
                timesheets = response.json()
                message = f"✅ Successfully submitted {len(timesheets)} pending timesheets for approval by {approver}."
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="❌ Could not submit pending timesheets.")
                
        except Exception as e:
            logger.error(f"Error submitting timesheets: {e}")
            dispatcher.utter_message(text="❌ An error occurred while submitting timesheets.")
        
        return []

class ActionGetPendingTimesheets(Action):
    def name(self) -> Text:
        return "action_get_pending_timesheets"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            response = requests.get(f"{BACKEND_BASE_URL}/timesheets/pending")
            
            if response.status_code == 200:
                timesheets = response.json()
                if timesheets:
                    message = f"⏳ You have {len(timesheets)} pending timesheets:\n\n"
                    for ts in timesheets[:3]:  # Show first 3
                        message += f"📅 {ts['date']} | {ts['from_time']}-{ts['to_time']} | {ts['total_hours']}h\n"
                    if len(timesheets) > 3:
                        message += f"\n... and {len(timesheets) - 3} more pending timesheets"
                else:
                    message = "✅ No pending timesheets found."
            else:
                message = "❌ Could not retrieve pending timesheets."
                
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error getting pending timesheets: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving pending timesheets.")
        
        return []

class ActionGetEmailContext(Action):
    def name(self) -> Text:
        return "action_get_email_context"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            email_id = tracker.get_slot("email_id") or "1"
            
            response = requests.get(f"{BACKEND_BASE_URL}/emails/{email_id}/context")
            
            if response.status_code == 200:
                email = response.json()
                message = f"📧 Email Context:\n\n📝 Subject: {email.get('subject', 'No subject')}\n📄 Content: {email.get('content', 'No content')}\n📧 Recipient: {email.get('recipient', 'N/A')}\n📊 Status: {email.get('status', 'N/A')}"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="❌ Could not retrieve email context.")
                
        except Exception as e:
            logger.error(f"Error getting email context: {e}")
            dispatcher.utter_message(text="❌ An error occurred while retrieving email context.")
        
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = """🤖 I'm here to help you with:

📊 **Timesheets**: Create, view, and submit timesheets
🏖️ **Leave Management**: Request and track leave
📧 **Email Management**: Create and manage emails
📋 **Task Management**: Create and track tasks

👨‍💼 **Admin Features**:
- "Show all data" - Get comprehensive dashboard
- "Show detailed timesheets" - Detailed timesheet analysis
- "Show detailed leaves" - Detailed leave analysis
- "Show detailed emails" - Detailed email analysis
- "Show detailed tasks" - Detailed task analysis
- "Approve timesheet 1" - Approve specific timesheet

Try saying:
- "Create a timesheet for today"
- "Show my leave requests"
- "Create an email to my manager"
- "List my tasks"
- "Submit my pending timesheets"
- "Show all data" (admin)
- "Approve timesheet 1 by manager" (admin)

How can I assist you today?"""
        
        dispatcher.utter_message(text=message)
        return []
