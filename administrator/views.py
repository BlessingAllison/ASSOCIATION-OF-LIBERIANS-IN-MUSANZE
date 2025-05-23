from django.shortcuts import render, reverse, redirect, get_object_or_404
from voting.models import Voter, Position, Candidate, Votes
from account.models import CustomUser
from account.forms import CustomUserForm
from voting.forms import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json  # Not used
import csv
from django_renderpdf.views import PDFView


def find_n_winners(data, n):
    """Read More
    https://www.geeksforgeeks.org/python-program-to-find-n-largest-elements-from-a-list/
    """
    final_list = []
    candidate_data = data[:]
    # print("Candidate = ", str(candidate_data))
    for i in range(0, n):
        max1 = 0
        if len(candidate_data) == 0:
            continue
        this_winner = max(candidate_data, key=lambda x: x['votes'])
        # TODO: Check if None
        this = this_winner['name'] + \
            " with " + str(this_winner['votes']) + " votes"
        final_list.append(this)
        candidate_data.remove(this_winner)
    return ", &nbsp;".join(final_list)


class PrintView(PDFView):
    template_name = 'admin/print.html'
    prompt_download = True

    @property
    def download_name(self):
        return "result.pdf"

    def get_context_data(self, *args, **kwargs):
        title = "E-voting"
        try:
            file = open(settings.ELECTION_TITLE_PATH, 'r')
            title = file.read()
        except:
            pass
        context = super().get_context_data(*args, **kwargs)
        position_data = {}
        for position in Position.objects.all():
            candidate_data = []
            winner = ""
            for candidate in Candidate.objects.filter(position=position):
                this_candidate_data = {}
                votes = Votes.objects.filter(candidate=candidate).count()
                this_candidate_data['name'] = candidate.fullname
                this_candidate_data['votes'] = votes
                candidate_data.append(this_candidate_data)
            print("Candidate Data For  ", str(
                position.name), " = ", str(candidate_data))
            # ! Check Winner
            if len(candidate_data) < 1:
                winner = "Position does not have candidates"
            else:
                # Check if max_vote is more than 1
                if position.max_vote > 1:
                    winner = find_n_winners(candidate_data, position.max_vote)
                else:

                    winner = max(candidate_data, key=lambda x: x['votes'])
                    if winner['votes'] == 0:
                        winner = "No one voted for this yet position, yet."
                    else:
                        """
                        https://stackoverflow.com/questions/18940540/how-can-i-count-the-occurrences-of-an-item-in-a-list-of-dictionaries
                        """
                        count = sum(1 for d in candidate_data if d.get(
                            'votes') == winner['votes'])
                        if count > 1:
                            winner = f"There are {count} candidates with {winner['votes']} votes"
                        else:
                            winner = "Winner : " + winner['name']
            print("Candidate Data For  ", str(
                position.name), " = ", str(candidate_data))
            position_data[position.name] = {
                'candidate_data': candidate_data, 'winner': winner, 'max_vote': position.max_vote}
        context['positions'] = position_data
        print(context)
        return context


def dashboard(request):
    positions = Position.objects.all().order_by('priority')
    candidates = Candidate.objects.all()
    voters = Voter.objects.all()
    voted_voters = Voter.objects.filter(voted=1)
    chart_data = {}

    for position in positions:
        candidates_data = []
        votes_data = []
        
        # Get all candidates for this position
        position_candidates = Candidate.objects.filter(position=position)
        
        for candidate in position_candidates:
            # Count votes for each candidate
            vote_count = Votes.objects.filter(candidate=candidate).count()
            candidates_data.append(candidate.fullname)
            votes_data.append(vote_count)
        
        # Store the data with position name as key
        chart_data[position.name] = {
            'candidates': candidates_data,
            'votes': votes_data,
            'pos_id': position.id,
            'slug': position.name.lower().replace(' ', '-')
        }

    context = {
        'position_count': positions.count(),
        'candidate_count': candidates.count(),
        'voters_count': voters.count(),
        'voted_voters_count': voted_voters.count(),
        'positions': positions,
        'chart_data': chart_data,
        'page_title': "Dashboard"
    }
    return render(request, "admin/home.html", context)


def voters(request):
    userForm = CustomUserForm()
    voterForm = VoterForm()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            userForm = CustomUserForm(request.POST)
            voterForm = VoterForm(request.POST, request.FILES)
            
            if userForm.is_valid() and voterForm.is_valid():
                user = userForm.save(commit=False)
                voter = voterForm.save(commit=False)
                voter.admin = user
                user.save()
                voter.save()
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Voter created successfully'
                    })
                return redirect('adminViewVoters')
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Form validation failed',
                        'errors': {
                            'user_form': userForm.errors,
                            'voter_form': voterForm.errors
                        }
                    }, status=400)
                messages.error(request, "Form validation failed")
                
        elif action == 'edit':
            voter_id = request.POST.get('edit_id')
            try:
                voter = Voter.objects.get(id=voter_id)
                user = voter.admin
                
                userForm = CustomUserForm(request.POST, instance=user)
                voterForm = VoterForm(request.POST, request.FILES, instance=voter)
                
                if userForm.is_valid() and voterForm.is_valid():
                    user = userForm.save()
                    voter = voterForm.save()
                    
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Voter updated successfully'
                        })
                    return redirect('adminViewVoters')
                else:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Form validation failed',
                            'errors': {
                                'user_form': userForm.errors,
                                'voter_form': voterForm.errors
                            }
                        }, status=400)
                    messages.error(request, "Form validation failed")
            except Voter.DoesNotExist:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Voter not found'
                    }, status=404)
                messages.error(request, "Voter not found")
                return redirect('adminViewVoters')
    
    voters = Voter.objects.all()
    context = {
        'form1': userForm,
        'form2': voterForm,
        'voters': voters,
        'page_title': 'Voters List'
    }
    return render(request, "admin/voters.html", context)


def view_voter_by_id(request):
    voter_id = request.GET.get('id', None)
    voter = Voter.objects.filter(id=voter_id)
    context = {}
    if not voter.exists():
        context['code'] = 404
        context['message'] = 'Voter not found'
        return JsonResponse(context, status=404)
    else:
        context['code'] = 200
        voter = voter[0]
        context['first_name'] = voter.admin.first_name
        context['last_name'] = voter.admin.last_name
        context['phone'] = voter.phone
        context['id'] = voter.id
        context['email'] = voter.admin.email
        context['photo'] = voter.photo.url if voter.photo else ''
        context['date_of_birth'] = voter.date_of_birth
        context['address'] = voter.address
        context['gender'] = voter.gender
        context['department'] = voter.department
        context['academic_level'] = voter.academic_level
        return JsonResponse(context)


def view_position_by_id(request):
    pos_id = request.GET.get('id', None)
    pos = Position.objects.filter(id=pos_id)
    context = {}
    if not pos.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        pos = pos[0]
        context['name'] = pos.name
        context['max_vote'] = pos.max_vote
        context['id'] = pos.id
    return JsonResponse(context)


def updateVoter(request, voter_id=None):
    if request.method == 'GET' and voter_id:
        try:
            # Handle GET request for viewing voter details
            voter = Voter.objects.get(id=voter_id)
            user = voter.admin
            context = {
                'voter': voter,
                'form': CustomUserForm(instance=user)
            }
            return render(request, 'admin/update_voter.html', context)
        except Voter.DoesNotExist:
            messages.error(request, "Voter not found")
            return redirect('administrator:adminViewVoters')
    
    elif request.method == 'POST':
        try:
            if not voter_id:
                voter_id = request.POST.get('id')
                if not voter_id:
                    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Voter ID is required'
                        }, status=400)
                    messages.error(request, "Voter ID is required")
                    return redirect('administrator:adminViewVoters')
            
            # Get the voter instance
            instance = Voter.objects.get(id=voter_id)
            
            # Create forms with the request data
            user_form = CustomUserForm(request.POST, instance=instance.admin)
            voter_form = VoterForm(request.POST, request.FILES, instance=instance)
            
            if user_form.is_valid() and voter_form.is_valid():
                user = user_form.save()
                voter = voter_form.save(commit=False)
                voter.admin = user
                voter.save()
                
                messages.success(request, "Voter updated successfully")
                if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Voter updated successfully'
                    })
                return redirect('administrator:adminViewVoters')
            else:
                error_messages = []
                if user_form.errors:
                    error_messages.extend(user_form.errors.values())
                if voter_form.errors:
                    error_messages.extend(voter_form.errors.values())
                
                error_message = " ".join([str(msg) for sublist in error_messages for msg in sublist])
                if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': error_message
                    }, status=400)
                
                messages.error(request, error_message)
                return redirect('administrator:adminViewVoters')
                
        except Voter.DoesNotExist:
            error_msg = "Voter not found"
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=404)
            messages.error(request, error_msg)
            return redirect('administrator:adminViewVoters')
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=500)
            messages.error(request, error_msg)
            return redirect('administrator:adminViewVoters')
    else:
        messages.error(request, "Invalid request method")
        return redirect('administrator:adminViewVoters')


def deleteVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        admin = Voter.objects.get(id=request.POST.get('id')).admin
        admin.delete()
        messages.success(request, "Voter Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewVoters'))


def viewPositions(request):
    positions = Position.objects.order_by('-priority').all()
    form = PositionForm(request.POST or None)
    context = {
        'positions': positions,
        'form1': form,
        'page_title': "Positions"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.priority = positions.count() + 1  # Just in case it is empty.
            form.save()
            messages.success(request, "New Position Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/positions.html", context)


def updatePosition(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Position.objects.get(id=request.POST.get('id'))
        pos = PositionForm(request.POST or None, instance=instance)
        pos.save()
        messages.success(request, "Position has been updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('administrator:viewPositions'))


def deletePosition(request):
    if request.method != 'POST':
        messages.error(request, "Access To This Resource Denied")
        return redirect(reverse('administrator:viewPositions'))
    try:
        pos = Position.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Position Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('administrator:viewPositions'))


def viewCandidates(request):
    candidates = Candidate.objects.all()
    form = CandidateForm(request.POST or None, request.FILES or None)
    context = {
        'candidates': candidates,
        'form1': form,
        'page_title': 'Candidates'
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save()
            messages.success(request, "New Candidate Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/candidates.html", context)


def updateCandidate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        candidate_id = request.POST.get('id')
        candidate = Candidate.objects.get(id=candidate_id)
        form = CandidateForm(request.POST or None,
                             request.FILES or None, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate Data Updated")
        else:
            messages.error(request, "Form has errors")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('administrator:viewCandidates'))


def deleteCandidate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect(reverse('administrator:viewCandidates'))
    try:
        pos = Candidate.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Candidate Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('administrator:viewCandidates'))


def view_candidate_by_id(request):
    candidate_id = request.GET.get('id', None)
    candidate = Candidate.objects.filter(id=candidate_id)
    context = {}
    if not candidate.exists():
        context['code'] = 404
    else:
        candidate = candidate[0]
        context['code'] = 200
        context['fullname'] = candidate.fullname
        previous = CandidateForm(instance=candidate)
        context['form'] = str(previous.as_p())
    return JsonResponse(context)


def ballot_position(request):
    context = {
        'page_title': "Ballot Position"
    }
    return render(request, "admin/ballot_position.html", context)


def update_ballot_position(request, position_id, up_or_down):
    try:
        context = {
            'error': False
        }
        position = Position.objects.get(id=position_id)
        if up_or_down == 'up':
            priority = position.priority - 1
            if priority == 0:
                context['error'] = True
                output = "This position is already at the top"
            else:
                Position.objects.filter(priority=priority).update(
                    priority=(priority+1))
                position.priority = priority
                position.save()
                output = "Moved Up"
        else:
            priority = position.priority + 1
            if priority > Position.objects.all().count():
                output = "This position is already at the bottom"
                context['error'] = True
            else:
                Position.objects.filter(priority=priority).update(
                    priority=(priority-1))
                position.priority = priority
                position.save()
                output = "Moved Down"
        context['message'] = output
    except Exception as e:
        context['message'] = e

    return JsonResponse(context)


def ballot_title(request):
    from urllib.parse import urlparse
    url = urlparse(request.META['HTTP_REFERER']).path
    from django.urls import resolve
    try:
        redirect_url = resolve(url)
        title = request.POST.get('title', 'No Name')
        file = open(settings.ELECTION_TITLE_PATH, 'w')
        file.write(title)
        file.close()
        messages.success(
            request, "Election title has been changed to " + str(title))
        return redirect(url)
    except Exception as e:
        messages.error(request, e)
        return redirect("/")


def viewVotes(request):
    votes = Votes.objects.all()
    context = {
        'votes': votes,
        'page_title': 'Votes'
    }
    return render(request, "admin/votes.html", context)


def resetVote(request):
    if request.method == 'POST':
        try:
            # Delete all votes
            Votes.objects.all().delete()
            # Reset all voters' voted status
            Voter.objects.all().update(voted=False, verified=False, otp=None)
            
            messages.success(request, "All votes have been reset successfully")
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'All votes have been reset successfully'
                })
            return redirect('administrator:viewVotes')
            
        except Exception as e:
            error_msg = f"An error occurred while resetting votes: {str(e)}"
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=500)
            messages.error(request, error_msg)
            return redirect('administrator:viewVotes')
    else:
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method'
            }, status=405)
        messages.error(request, "Invalid request method")
        return redirect('administrator:viewVotes')


def result(request):
    """
    Display the election results
    """
    context = {
        'page_title': 'Election Results',
    }
    return render(request, 'admin/result.html', context)


def compute_candidate_vote(request, position_id=None):
    """
    Compute and return the vote count for a specific position
    """
    position = get_object_or_404(Position, id=position_id)
    candidates = Candidate.objects.filter(position=position)
    # Add your vote computation logic here
    return JsonResponse({'status': 'success'})


def export_voters_votes(request):
    """
    Export voters' votes to a file (CSV/Excel)
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voting_results.csv"'
    
    # Add your export logic here
    writer = csv.writer(response)
    writer.writerow(['Voter ID', 'Voter Name', 'Position', 'Candidate Voted', 'Date Voted'])
    
    return response
