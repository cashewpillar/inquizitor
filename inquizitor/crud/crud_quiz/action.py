from sqlmodel import Session
from typing import Any, Dict, List, Union
import pandas as pd
import joblib
import logging
import pprint
import random

from inquizitor.crud.base import CRUDBase
from inquizitor.models import QuizAttempt, QuizAction, QuizActionCreate, QuizActionUpdate

class CRUDQuizAction(CRUDBase[QuizAction, QuizActionCreate, QuizActionUpdate]):
    def update(self, db: Session, *, db_obj: QuizAction, obj_in: Union[QuizActionUpdate, Dict[str, Any]]) -> None:
        raise Exception('QuizAction does not allow updating of records')

    def get_multi_by_question_attempt(
        self, db: Session, *, question_id: int, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(
                QuizAction.question_id == question_id,
                QuizAction.attempt_id == attempt_id
            )
            .all()
        )

    def get_multi_by_attempt(
        self, db: Session, *, attempt_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(QuizAction.attempt_id == attempt_id)
            .all()
        )

    def get_multi_by_question(
        self, db: Session, *, question_id: int
    ) -> List[QuizAction]:
        return (
            db.query(QuizAction)
            .filter(QuizAction.question_id == question_id)
            .all()
        )

    def get_multi_by_quiz_order_by_student(
        self, db: Session, *, quiz_id: int
    ) -> List[QuizAction]:
        """Get quiz actions, order by student"""
        return (
            db.query(QuizAction)
            .join(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.student_id)
            .all()
        )

    def get_multi_by_attempt_order_by_question(
        self, db: Session, *, attempt_id: int
    ) -> List[QuizAction]:
        """Get quiz actions for the given student attempt, order by question"""
        return (
            db.query(QuizAction)
            .filter(QuizAction.attempt_id == attempt_id)
            .order_by(QuizAction.question_id)
            .all()
        )

    def get_per_student_summary_by_quiz(
        self, db: Session, *, quiz_id: int
    ) -> Any:
        """Get per-student summary of actions for the given quiz"""
        summary = dict()
        actions = (
            db.query(QuizAction)
            .join(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz_id)
            .order_by(QuizAttempt.student_id)
            .all()
        )
        action_list = {
            'blur': 0,
            'focus': 0,
            'copy_': 0,
            'paste': 0,
            'left_click': 0,
            'right_click': 0,
            'double_click': 0,
        }
        for action in actions:
            student_name = action.attempt.student.username
            summary.setdefault(student_name, dict(action_list))
            summary[student_name]['blur'] += action.blur
            summary[student_name]['focus'] += action.focus
            summary[student_name]['copy_'] += action.copy_
            summary[student_name]['paste'] += action.paste
            summary[student_name]['left_click'] += action.left_click
            summary[student_name]['right_click'] += action.right_click
            summary[student_name]['double_click'] += action.double_click

        return summary

    # ============================================================================
    #                       [WIP] MACHINE LEARNING METHODS
    # ============================================================================

    def aggregate_actions(self, df):
        return df.drop(columns=['time']).groupby(['attempt_id', 'question_id'], as_index=False).sum()

    def with_inactive_duration(self, df):
        df_aggregated = self.aggregate_actions(df)
        
        # declare duration
        duration = 0
        
        # get the (not aggregated) events of the user (so we can take a look at each event)
        user_events = df.sort_values(by=['time'])
        
        # get the questions ids that the user answered
        question_ids = user_events['question_id'].unique()

        # calculate the duration for each question
        for question_id in question_ids:
            
            # get only the events for the current question id
            user_events_by_question = user_events[user_events.question_id == question_id]
            
            # check each event for the current question id
            for i in range(len(user_events_by_question)):
            
                # skip first action
                if i == 0:
                    continue  

                # if PREVIOUS action is blur,
                # compute the duration (in seconds) it took before the CURRENT action occured
                # then increase the total duration by adding the computed value 
                if user_events_by_question.iloc[i - 1]['blur'] == 1:
                    time_difference = pd.to_datetime(user_events_by_question.iloc[i]['time']) - pd.to_datetime(user_events_by_question.iloc[i - 1]['time'])
                    duration = duration + time_difference.total_seconds()
                
            # after all events have been iterated,
            # add column of inactive duration with the value of total inactive duration in seconds
            df_aggregated.loc[(df_aggregated.question_id == question_id), 'inactive_duration'] = duration
                
            # reset duration to 0 
            duration = 0
        
        return df_aggregated.drop(columns=['attempt_id', 'question_id'])

    def predict(self, sample):
        # load model
        s = joblib.load('thesis_model.pkl') # is it ideal to load every time?

        return s.predict(sample) #output /-> array([False, False])

    def get_per_question_summary_by_attempt(
        self, db: Session, *, attempt_id: int, get_predictions: bool = False
    ) -> Any:
        """Get per-question summary of actions for the given attempt"""
        summary = dict()
        actions = (
            db.query(QuizAction)
            .filter(QuizAction.attempt_id == attempt_id)
            .order_by(QuizAction.question_id)
            .all()
        )

        if get_predictions:
            # NOT ELEGANT BUT FLAWLESS
            attempt_id = [action.attempt_id for action in actions]
            question_id = [action.question_id for action in actions]
            blur = [action.blur for action in actions]
            focus = [action.focus for action in actions]
            copy = [action.copy_ for action in actions]
            paste = [action.paste for action in actions]
            left_click = [action.left_click for action in actions]
            right_click = [action.right_click for action in actions]
            double_click = [action.double_click for action in actions]
            time = [action.time for action in actions]
            zipped = list(zip(attempt_id, question_id, blur, focus, copy, paste, left_click, right_click, double_click, time))
            actions_df = pd.DataFrame(zipped, columns=['attempt_id', 'question_id', 'blur', 'focus', 'copy', 'paste', 'left_click', 'right_click', 'double_click', 'time'])
            
            # ELEGANT BUT ERRONEOUS
            # actions_df = pd.DataFrame(actions)
            # actions_df.columns = ['type', 'question_id', 'attempt_id', 'blur', 'copy', 'left_click', 'double_click', 'event_id', 'time', 'focus', 'paste', 'right_click']
            # actions_df = actions_df.loc[:, ~actions_df.columns.isin(['type', 'event_id'])]
            # actions_df = actions_df.apply(
            #     lambda row: row.apply(lambda cell: cell[1]), # extract y value from the tuple (x, y)
            #     axis=1
            # )
            # actions_df = actions_df[['attempt_id', 'question_id', 'blur', 'focus', 'copy', 'paste', 'left_click', 'right_click', 'double_click', 'time']]
            
            sample = self.with_inactive_duration(actions_df)
            inactive_durations = sample['inactive_duration']
            predictions = list(self.predict(sample))

        action_list = {
            'blur': 0,
            'focus': 0,
            'copy_': 0,
            'paste': 0,
            'left_click': 0,
            'right_click': 0,
            'double_click': 0,
        }
        for action in actions:
            question_id = action.question_id
            summary.setdefault(question_id, dict(action_list))
            summary[question_id]['blur'] += action.blur
            summary[question_id]['focus'] += action.focus
            summary[question_id]['copy_'] += action.copy_
            summary[question_id]['paste'] += action.paste
            summary[question_id]['left_click'] += action.left_click
            summary[question_id]['right_click'] += action.right_click
            summary[question_id]['double_click'] += action.double_click
        
        if get_predictions:
            for i, question_id in enumerate(summary.keys()):
                summary[question_id]['inactive_duration'] = inactive_durations[i]
                summary[question_id]['label'] = bool(predictions[i])

        return summary

quiz_action = CRUDQuizAction(QuizAction)
