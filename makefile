all: clean vetting bad_cooperation_list

clean:
	@rm -rf cs330e-diplomacy-tests
	@rm -rf repos
	@rm -rf output

vetting:
	@python DiplomacyVetting.py
	
bad_cooperation_list:
	@python DiplomacyCheckCooperationPoints.py