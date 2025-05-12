from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="adminDashboard"),
    # * Voters
    path('voters/', views.voters, name="adminViewVoters"),
    path('voters/view/', views.voters, name='viewVoters'),
    path('voters/update/<int:voter_id>/', views.updateVoter, name='updateVoter'),
    path('voters/update/', views.updateVoter, name='updateVoterPost'),  # For POST requests without ID in URL
    path('voters/delete/', views.deleteVoter, name='deleteVoter'),

    # * Position
    path('position/view/', views.view_position_by_id, name="viewPosition"),
    path('position/update/', views.updatePosition, name="updatePosition"),
    path('position/delete/', views.deletePosition, name='deletePosition'),
    path('positions/view/', views.viewPositions, name='viewPositions'),

    # * Candidate
    path('candidate/', views.viewCandidates, name='viewCandidates'),
    path('candidate/update/', views.updateCandidate, name="updateCandidate"),
    path('candidate/delete/', views.deleteCandidate, name='deleteCandidate'),
    path('candidate/view/', views.view_candidate_by_id, name='viewCandidate'),

    # * Settings (Ballot Position and Election Title)
    path("settings/ballot/position/", views.ballot_position, name='ballot_position'),
    path("settings/ballot/title/", views.ballot_title, name='ballot_title'),
    path("settings/ballot/position/update/<int:position_id>/<str:up_or_down>/",
         views.update_ballot_position, name='update_ballot_position'),

    # * Votes
    path('votes/view/', views.viewVotes, name="viewVotes"),
    path('votes/reset/', views.resetVote, name='resetVote'),  
    path('votes/print/', views.PrintView.as_view(), name='printResult'),
    path('votes/result/', views.result, name='result'),
    path('votes/result/position/<int:position_id>/', views.compute_candidate_vote, name='compute_candidate_vote'),
    path('votes/export/', views.export_voters_votes, name='export_voters_votes'),
]
