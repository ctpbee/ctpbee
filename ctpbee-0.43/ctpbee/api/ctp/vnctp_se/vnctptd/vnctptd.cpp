// vnctpmd.cpp : 定义 DLL 应用程序的导出函数。
//

#include "vnctptdApp.h"


///-------------------------------------------------------------------------------------
///C++的回调函数将数据保存到队列中
///-------------------------------------------------------------------------------------

void TdApiApp::OnFrontConnected()
{
	Task task = Task();
	task.task_name = ONFRONTCONNECTED;
	this->task_queue.push(task);
};

void TdApiApp::OnFrontDisconnected(int nReason)
{
	Task task = Task();
	task.task_name = ONFRONTDISCONNECTED;
	task.task_id = nReason;
	this->task_queue.push(task);
};

void TdApiApp::OnHeartBeatWarning(int nTimeLapse)
{
	Task task = Task();
	task.task_name = ONHEARTBEATWARNING;
	task.task_id = nTimeLapse;
	this->task_queue.push(task);
};

void TdApiApp::OnRspAuthenticate(CThostFtdcRspAuthenticateField *pRspAuthenticateField, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPAUTHENTICATE;
	if (pRspAuthenticateField)
	{
		CThostFtdcRspAuthenticateField *task_data = new CThostFtdcRspAuthenticateField();
		*task_data = *pRspAuthenticateField;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPUSERLOGIN;
	if (pRspUserLogin)
	{
		CThostFtdcRspUserLoginField *task_data = new CThostFtdcRspUserLoginField();
		*task_data = *pRspUserLogin;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPUSERLOGOUT;
	if (pUserLogout)
	{
		CThostFtdcUserLogoutField *task_data = new CThostFtdcUserLogoutField();
		*task_data = *pUserLogout;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspUserPasswordUpdate(CThostFtdcUserPasswordUpdateField *pUserPasswordUpdate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPUSERPASSWORDUPDATE;
	if (pUserPasswordUpdate)
	{
		CThostFtdcUserPasswordUpdateField *task_data = new CThostFtdcUserPasswordUpdateField();
		*task_data = *pUserPasswordUpdate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspTradingAccountPasswordUpdate(CThostFtdcTradingAccountPasswordUpdateField *pTradingAccountPasswordUpdate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPTRADINGACCOUNTPASSWORDUPDATE;
	if (pTradingAccountPasswordUpdate)
	{
		CThostFtdcTradingAccountPasswordUpdateField *task_data = new CThostFtdcTradingAccountPasswordUpdateField();
		*task_data = *pTradingAccountPasswordUpdate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspUserAuthMethod(CThostFtdcRspUserAuthMethodField *pRspUserAuthMethod, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPUSERAUTHMETHOD;
	if (pRspUserAuthMethod)
	{
		CThostFtdcRspUserAuthMethodField *task_data = new CThostFtdcRspUserAuthMethodField();
		*task_data = *pRspUserAuthMethod;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspGenUserCaptcha(CThostFtdcRspGenUserCaptchaField *pRspGenUserCaptcha, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPGENUSERCAPTCHA;
	if (pRspGenUserCaptcha)
	{
		CThostFtdcRspGenUserCaptchaField *task_data = new CThostFtdcRspGenUserCaptchaField();
		*task_data = *pRspGenUserCaptcha;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspGenUserText(CThostFtdcRspGenUserTextField *pRspGenUserText, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPGENUSERTEXT;
	if (pRspGenUserText)
	{
		CThostFtdcRspGenUserTextField *task_data = new CThostFtdcRspGenUserTextField();
		*task_data = *pRspGenUserText;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspOrderInsert(CThostFtdcInputOrderField *pInputOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPORDERINSERT;
	if (pInputOrder)
	{
		CThostFtdcInputOrderField *task_data = new CThostFtdcInputOrderField();
		*task_data = *pInputOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspParkedOrderInsert(CThostFtdcParkedOrderField *pParkedOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPPARKEDORDERINSERT;
	if (pParkedOrder)
	{
		CThostFtdcParkedOrderField *task_data = new CThostFtdcParkedOrderField();
		*task_data = *pParkedOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspParkedOrderAction(CThostFtdcParkedOrderActionField *pParkedOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPPARKEDORDERACTION;
	if (pParkedOrderAction)
	{
		CThostFtdcParkedOrderActionField *task_data = new CThostFtdcParkedOrderActionField();
		*task_data = *pParkedOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspOrderAction(CThostFtdcInputOrderActionField *pInputOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPORDERACTION;
	if (pInputOrderAction)
	{
		CThostFtdcInputOrderActionField *task_data = new CThostFtdcInputOrderActionField();
		*task_data = *pInputOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQueryMaxOrderVolume(CThostFtdcQueryMaxOrderVolumeField *pQueryMaxOrderVolume, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQUERYMAXORDERVOLUME;
	if (pQueryMaxOrderVolume)
	{
		CThostFtdcQueryMaxOrderVolumeField *task_data = new CThostFtdcQueryMaxOrderVolumeField();
		*task_data = *pQueryMaxOrderVolume;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPSETTLEMENTINFOCONFIRM;
	if (pSettlementInfoConfirm)
	{
		CThostFtdcSettlementInfoConfirmField *task_data = new CThostFtdcSettlementInfoConfirmField();
		*task_data = *pSettlementInfoConfirm;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspRemoveParkedOrder(CThostFtdcRemoveParkedOrderField *pRemoveParkedOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPREMOVEPARKEDORDER;
	if (pRemoveParkedOrder)
	{
		CThostFtdcRemoveParkedOrderField *task_data = new CThostFtdcRemoveParkedOrderField();
		*task_data = *pRemoveParkedOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspRemoveParkedOrderAction(CThostFtdcRemoveParkedOrderActionField *pRemoveParkedOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPREMOVEPARKEDORDERACTION;
	if (pRemoveParkedOrderAction)
	{
		CThostFtdcRemoveParkedOrderActionField *task_data = new CThostFtdcRemoveParkedOrderActionField();
		*task_data = *pRemoveParkedOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspExecOrderInsert(CThostFtdcInputExecOrderField *pInputExecOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPEXECORDERINSERT;
	if (pInputExecOrder)
	{
		CThostFtdcInputExecOrderField *task_data = new CThostFtdcInputExecOrderField();
		*task_data = *pInputExecOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspExecOrderAction(CThostFtdcInputExecOrderActionField *pInputExecOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPEXECORDERACTION;
	if (pInputExecOrderAction)
	{
		CThostFtdcInputExecOrderActionField *task_data = new CThostFtdcInputExecOrderActionField();
		*task_data = *pInputExecOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspForQuoteInsert(CThostFtdcInputForQuoteField *pInputForQuote, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPFORQUOTEINSERT;
	if (pInputForQuote)
	{
		CThostFtdcInputForQuoteField *task_data = new CThostFtdcInputForQuoteField();
		*task_data = *pInputForQuote;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQuoteInsert(CThostFtdcInputQuoteField *pInputQuote, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQUOTEINSERT;
	if (pInputQuote)
	{
		CThostFtdcInputQuoteField *task_data = new CThostFtdcInputQuoteField();
		*task_data = *pInputQuote;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQuoteAction(CThostFtdcInputQuoteActionField *pInputQuoteAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQUOTEACTION;
	if (pInputQuoteAction)
	{
		CThostFtdcInputQuoteActionField *task_data = new CThostFtdcInputQuoteActionField();
		*task_data = *pInputQuoteAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspBatchOrderAction(CThostFtdcInputBatchOrderActionField *pInputBatchOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPBATCHORDERACTION;
	if (pInputBatchOrderAction)
	{
		CThostFtdcInputBatchOrderActionField *task_data = new CThostFtdcInputBatchOrderActionField();
		*task_data = *pInputBatchOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspOptionSelfCloseInsert(CThostFtdcInputOptionSelfCloseField *pInputOptionSelfClose, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPOPTIONSELFCLOSEINSERT;
	if (pInputOptionSelfClose)
	{
		CThostFtdcInputOptionSelfCloseField *task_data = new CThostFtdcInputOptionSelfCloseField();
		*task_data = *pInputOptionSelfClose;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspOptionSelfCloseAction(CThostFtdcInputOptionSelfCloseActionField *pInputOptionSelfCloseAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPOPTIONSELFCLOSEACTION;
	if (pInputOptionSelfCloseAction)
	{
		CThostFtdcInputOptionSelfCloseActionField *task_data = new CThostFtdcInputOptionSelfCloseActionField();
		*task_data = *pInputOptionSelfCloseAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspCombActionInsert(CThostFtdcInputCombActionField *pInputCombAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPCOMBACTIONINSERT;
	if (pInputCombAction)
	{
		CThostFtdcInputCombActionField *task_data = new CThostFtdcInputCombActionField();
		*task_data = *pInputCombAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryOrder(CThostFtdcOrderField *pOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYORDER;
	if (pOrder)
	{
		CThostFtdcOrderField *task_data = new CThostFtdcOrderField();
		*task_data = *pOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryTrade(CThostFtdcTradeField *pTrade, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYTRADE;
	if (pTrade)
	{
		CThostFtdcTradeField *task_data = new CThostFtdcTradeField();
		*task_data = *pTrade;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINVESTORPOSITION;
	if (pInvestorPosition)
	{
		CThostFtdcInvestorPositionField *task_data = new CThostFtdcInvestorPositionField();
		*task_data = *pInvestorPosition;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYTRADINGACCOUNT;
	if (pTradingAccount)
	{
		CThostFtdcTradingAccountField *task_data = new CThostFtdcTradingAccountField();
		*task_data = *pTradingAccount;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInvestor(CThostFtdcInvestorField *pInvestor, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINVESTOR;
	if (pInvestor)
	{
		CThostFtdcInvestorField *task_data = new CThostFtdcInvestorField();
		*task_data = *pInvestor;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryTradingCode(CThostFtdcTradingCodeField *pTradingCode, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYTRADINGCODE;
	if (pTradingCode)
	{
		CThostFtdcTradingCodeField *task_data = new CThostFtdcTradingCodeField();
		*task_data = *pTradingCode;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInstrumentMarginRate(CThostFtdcInstrumentMarginRateField *pInstrumentMarginRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINSTRUMENTMARGINRATE;
	if (pInstrumentMarginRate)
	{
		CThostFtdcInstrumentMarginRateField *task_data = new CThostFtdcInstrumentMarginRateField();
		*task_data = *pInstrumentMarginRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInstrumentCommissionRate(CThostFtdcInstrumentCommissionRateField *pInstrumentCommissionRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINSTRUMENTCOMMISSIONRATE;
	if (pInstrumentCommissionRate)
	{
		CThostFtdcInstrumentCommissionRateField *task_data = new CThostFtdcInstrumentCommissionRateField();
		*task_data = *pInstrumentCommissionRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryExchange(CThostFtdcExchangeField *pExchange, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYEXCHANGE;
	if (pExchange)
	{
		CThostFtdcExchangeField *task_data = new CThostFtdcExchangeField();
		*task_data = *pExchange;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryProduct(CThostFtdcProductField *pProduct, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYPRODUCT;
	if (pProduct)
	{
		CThostFtdcProductField *task_data = new CThostFtdcProductField();
		*task_data = *pProduct;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInstrument(CThostFtdcInstrumentField *pInstrument, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINSTRUMENT;
	if (pInstrument)
	{
		CThostFtdcInstrumentField *task_data = new CThostFtdcInstrumentField();
		*task_data = *pInstrument;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYDEPTHMARKETDATA;
	if (pDepthMarketData)
	{
		CThostFtdcDepthMarketDataField *task_data = new CThostFtdcDepthMarketDataField();
		*task_data = *pDepthMarketData;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQrySettlementInfo(CThostFtdcSettlementInfoField *pSettlementInfo, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYSETTLEMENTINFO;
	if (pSettlementInfo)
	{
		CThostFtdcSettlementInfoField *task_data = new CThostFtdcSettlementInfoField();
		*task_data = *pSettlementInfo;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryTransferBank(CThostFtdcTransferBankField *pTransferBank, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYTRANSFERBANK;
	if (pTransferBank)
	{
		CThostFtdcTransferBankField *task_data = new CThostFtdcTransferBankField();
		*task_data = *pTransferBank;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInvestorPositionDetail(CThostFtdcInvestorPositionDetailField *pInvestorPositionDetail, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINVESTORPOSITIONDETAIL;
	if (pInvestorPositionDetail)
	{
		CThostFtdcInvestorPositionDetailField *task_data = new CThostFtdcInvestorPositionDetailField();
		*task_data = *pInvestorPositionDetail;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryNotice(CThostFtdcNoticeField *pNotice, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYNOTICE;
	if (pNotice)
	{
		CThostFtdcNoticeField *task_data = new CThostFtdcNoticeField();
		*task_data = *pNotice;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQrySettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYSETTLEMENTINFOCONFIRM;
	if (pSettlementInfoConfirm)
	{
		CThostFtdcSettlementInfoConfirmField *task_data = new CThostFtdcSettlementInfoConfirmField();
		*task_data = *pSettlementInfoConfirm;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInvestorPositionCombineDetail(CThostFtdcInvestorPositionCombineDetailField *pInvestorPositionCombineDetail, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINVESTORPOSITIONCOMBINEDETAIL;
	if (pInvestorPositionCombineDetail)
	{
		CThostFtdcInvestorPositionCombineDetailField *task_data = new CThostFtdcInvestorPositionCombineDetailField();
		*task_data = *pInvestorPositionCombineDetail;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryCFMMCTradingAccountKey(CThostFtdcCFMMCTradingAccountKeyField *pCFMMCTradingAccountKey, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYCFMMCTRADINGACCOUNTKEY;
	if (pCFMMCTradingAccountKey)
	{
		CThostFtdcCFMMCTradingAccountKeyField *task_data = new CThostFtdcCFMMCTradingAccountKeyField();
		*task_data = *pCFMMCTradingAccountKey;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryEWarrantOffset(CThostFtdcEWarrantOffsetField *pEWarrantOffset, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYEWARRANTOFFSET;
	if (pEWarrantOffset)
	{
		CThostFtdcEWarrantOffsetField *task_data = new CThostFtdcEWarrantOffsetField();
		*task_data = *pEWarrantOffset;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInvestorProductGroupMargin(CThostFtdcInvestorProductGroupMarginField *pInvestorProductGroupMargin, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINVESTORPRODUCTGROUPMARGIN;
	if (pInvestorProductGroupMargin)
	{
		CThostFtdcInvestorProductGroupMarginField *task_data = new CThostFtdcInvestorProductGroupMarginField();
		*task_data = *pInvestorProductGroupMargin;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryExchangeMarginRate(CThostFtdcExchangeMarginRateField *pExchangeMarginRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYEXCHANGEMARGINRATE;
	if (pExchangeMarginRate)
	{
		CThostFtdcExchangeMarginRateField *task_data = new CThostFtdcExchangeMarginRateField();
		*task_data = *pExchangeMarginRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryExchangeMarginRateAdjust(CThostFtdcExchangeMarginRateAdjustField *pExchangeMarginRateAdjust, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYEXCHANGEMARGINRATEADJUST;
	if (pExchangeMarginRateAdjust)
	{
		CThostFtdcExchangeMarginRateAdjustField *task_data = new CThostFtdcExchangeMarginRateAdjustField();
		*task_data = *pExchangeMarginRateAdjust;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryExchangeRate(CThostFtdcExchangeRateField *pExchangeRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYEXCHANGERATE;
	if (pExchangeRate)
	{
		CThostFtdcExchangeRateField *task_data = new CThostFtdcExchangeRateField();
		*task_data = *pExchangeRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQrySecAgentACIDMap(CThostFtdcSecAgentACIDMapField *pSecAgentACIDMap, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYSECAGENTACIDMAP;
	if (pSecAgentACIDMap)
	{
		CThostFtdcSecAgentACIDMapField *task_data = new CThostFtdcSecAgentACIDMapField();
		*task_data = *pSecAgentACIDMap;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryProductExchRate(CThostFtdcProductExchRateField *pProductExchRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYPRODUCTEXCHRATE;
	if (pProductExchRate)
	{
		CThostFtdcProductExchRateField *task_data = new CThostFtdcProductExchRateField();
		*task_data = *pProductExchRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryProductGroup(CThostFtdcProductGroupField *pProductGroup, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYPRODUCTGROUP;
	if (pProductGroup)
	{
		CThostFtdcProductGroupField *task_data = new CThostFtdcProductGroupField();
		*task_data = *pProductGroup;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryMMInstrumentCommissionRate(CThostFtdcMMInstrumentCommissionRateField *pMMInstrumentCommissionRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYMMINSTRUMENTCOMMISSIONRATE;
	if (pMMInstrumentCommissionRate)
	{
		CThostFtdcMMInstrumentCommissionRateField *task_data = new CThostFtdcMMInstrumentCommissionRateField();
		*task_data = *pMMInstrumentCommissionRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryMMOptionInstrCommRate(CThostFtdcMMOptionInstrCommRateField *pMMOptionInstrCommRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYMMOPTIONINSTRCOMMRATE;
	if (pMMOptionInstrCommRate)
	{
		CThostFtdcMMOptionInstrCommRateField *task_data = new CThostFtdcMMOptionInstrCommRateField();
		*task_data = *pMMOptionInstrCommRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInstrumentOrderCommRate(CThostFtdcInstrumentOrderCommRateField *pInstrumentOrderCommRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINSTRUMENTORDERCOMMRATE;
	if (pInstrumentOrderCommRate)
	{
		CThostFtdcInstrumentOrderCommRateField *task_data = new CThostFtdcInstrumentOrderCommRateField();
		*task_data = *pInstrumentOrderCommRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQrySecAgentTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYSECAGENTTRADINGACCOUNT;
	if (pTradingAccount)
	{
		CThostFtdcTradingAccountField *task_data = new CThostFtdcTradingAccountField();
		*task_data = *pTradingAccount;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQrySecAgentCheckMode(CThostFtdcSecAgentCheckModeField *pSecAgentCheckMode, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYSECAGENTCHECKMODE;
	if (pSecAgentCheckMode)
	{
		CThostFtdcSecAgentCheckModeField *task_data = new CThostFtdcSecAgentCheckModeField();
		*task_data = *pSecAgentCheckMode;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQrySecAgentTradeInfo(CThostFtdcSecAgentTradeInfoField *pSecAgentTradeInfo, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYSECAGENTTRADEINFO;
	if (pSecAgentTradeInfo)
	{
		CThostFtdcSecAgentTradeInfoField *task_data = new CThostFtdcSecAgentTradeInfoField();
		*task_data = *pSecAgentTradeInfo;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryOptionInstrTradeCost(CThostFtdcOptionInstrTradeCostField *pOptionInstrTradeCost, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYOPTIONINSTRTRADECOST;
	if (pOptionInstrTradeCost)
	{
		CThostFtdcOptionInstrTradeCostField *task_data = new CThostFtdcOptionInstrTradeCostField();
		*task_data = *pOptionInstrTradeCost;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryOptionInstrCommRate(CThostFtdcOptionInstrCommRateField *pOptionInstrCommRate, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYOPTIONINSTRCOMMRATE;
	if (pOptionInstrCommRate)
	{
		CThostFtdcOptionInstrCommRateField *task_data = new CThostFtdcOptionInstrCommRateField();
		*task_data = *pOptionInstrCommRate;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryExecOrder(CThostFtdcExecOrderField *pExecOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYEXECORDER;
	if (pExecOrder)
	{
		CThostFtdcExecOrderField *task_data = new CThostFtdcExecOrderField();
		*task_data = *pExecOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryForQuote(CThostFtdcForQuoteField *pForQuote, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYFORQUOTE;
	if (pForQuote)
	{
		CThostFtdcForQuoteField *task_data = new CThostFtdcForQuoteField();
		*task_data = *pForQuote;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryQuote(CThostFtdcQuoteField *pQuote, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYQUOTE;
	if (pQuote)
	{
		CThostFtdcQuoteField *task_data = new CThostFtdcQuoteField();
		*task_data = *pQuote;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryOptionSelfClose(CThostFtdcOptionSelfCloseField *pOptionSelfClose, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYOPTIONSELFCLOSE;
	if (pOptionSelfClose)
	{
		CThostFtdcOptionSelfCloseField *task_data = new CThostFtdcOptionSelfCloseField();
		*task_data = *pOptionSelfClose;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryInvestUnit(CThostFtdcInvestUnitField *pInvestUnit, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYINVESTUNIT;
	if (pInvestUnit)
	{
		CThostFtdcInvestUnitField *task_data = new CThostFtdcInvestUnitField();
		*task_data = *pInvestUnit;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryCombInstrumentGuard(CThostFtdcCombInstrumentGuardField *pCombInstrumentGuard, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYCOMBINSTRUMENTGUARD;
	if (pCombInstrumentGuard)
	{
		CThostFtdcCombInstrumentGuardField *task_data = new CThostFtdcCombInstrumentGuardField();
		*task_data = *pCombInstrumentGuard;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryCombAction(CThostFtdcCombActionField *pCombAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYCOMBACTION;
	if (pCombAction)
	{
		CThostFtdcCombActionField *task_data = new CThostFtdcCombActionField();
		*task_data = *pCombAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryTransferSerial(CThostFtdcTransferSerialField *pTransferSerial, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYTRANSFERSERIAL;
	if (pTransferSerial)
	{
		CThostFtdcTransferSerialField *task_data = new CThostFtdcTransferSerialField();
		*task_data = *pTransferSerial;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryAccountregister(CThostFtdcAccountregisterField *pAccountregister, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYACCOUNTREGISTER;
	if (pAccountregister)
	{
		CThostFtdcAccountregisterField *task_data = new CThostFtdcAccountregisterField();
		*task_data = *pAccountregister;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspError(CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPERROR;
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRtnOrder(CThostFtdcOrderField *pOrder)
{
	Task task = Task();
	task.task_name = ONRTNORDER;
	if (pOrder)
	{
		CThostFtdcOrderField *task_data = new CThostFtdcOrderField();
		*task_data = *pOrder;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnTrade(CThostFtdcTradeField *pTrade)
{
	Task task = Task();
	task.task_name = ONRTNTRADE;
	if (pTrade)
	{
		CThostFtdcTradeField *task_data = new CThostFtdcTradeField();
		*task_data = *pTrade;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnOrderInsert(CThostFtdcInputOrderField *pInputOrder, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNORDERINSERT;
	if (pInputOrder)
	{
		CThostFtdcInputOrderField *task_data = new CThostFtdcInputOrderField();
		*task_data = *pInputOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnOrderAction(CThostFtdcOrderActionField *pOrderAction, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNORDERACTION;
	if (pOrderAction)
	{
		CThostFtdcOrderActionField *task_data = new CThostFtdcOrderActionField();
		*task_data = *pOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnInstrumentStatus(CThostFtdcInstrumentStatusField *pInstrumentStatus)
{
	Task task = Task();
	task.task_name = ONRTNINSTRUMENTSTATUS;
	if (pInstrumentStatus)
	{
		CThostFtdcInstrumentStatusField *task_data = new CThostFtdcInstrumentStatusField();
		*task_data = *pInstrumentStatus;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnBulletin(CThostFtdcBulletinField *pBulletin)
{
	Task task = Task();
	task.task_name = ONRTNBULLETIN;
	if (pBulletin)
	{
		CThostFtdcBulletinField *task_data = new CThostFtdcBulletinField();
		*task_data = *pBulletin;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnTradingNotice(CThostFtdcTradingNoticeInfoField *pTradingNoticeInfo)
{
	Task task = Task();
	task.task_name = ONRTNTRADINGNOTICE;
	if (pTradingNoticeInfo)
	{
		CThostFtdcTradingNoticeInfoField *task_data = new CThostFtdcTradingNoticeInfoField();
		*task_data = *pTradingNoticeInfo;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnErrorConditionalOrder(CThostFtdcErrorConditionalOrderField *pErrorConditionalOrder)
{
	Task task = Task();
	task.task_name = ONRTNERRORCONDITIONALORDER;
	if (pErrorConditionalOrder)
	{
		CThostFtdcErrorConditionalOrderField *task_data = new CThostFtdcErrorConditionalOrderField();
		*task_data = *pErrorConditionalOrder;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnExecOrder(CThostFtdcExecOrderField *pExecOrder)
{
	Task task = Task();
	task.task_name = ONRTNEXECORDER;
	if (pExecOrder)
	{
		CThostFtdcExecOrderField *task_data = new CThostFtdcExecOrderField();
		*task_data = *pExecOrder;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnExecOrderInsert(CThostFtdcInputExecOrderField *pInputExecOrder, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNEXECORDERINSERT;
	if (pInputExecOrder)
	{
		CThostFtdcInputExecOrderField *task_data = new CThostFtdcInputExecOrderField();
		*task_data = *pInputExecOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnExecOrderAction(CThostFtdcExecOrderActionField *pExecOrderAction, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNEXECORDERACTION;
	if (pExecOrderAction)
	{
		CThostFtdcExecOrderActionField *task_data = new CThostFtdcExecOrderActionField();
		*task_data = *pExecOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnForQuoteInsert(CThostFtdcInputForQuoteField *pInputForQuote, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNFORQUOTEINSERT;
	if (pInputForQuote)
	{
		CThostFtdcInputForQuoteField *task_data = new CThostFtdcInputForQuoteField();
		*task_data = *pInputForQuote;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnQuote(CThostFtdcQuoteField *pQuote)
{
	Task task = Task();
	task.task_name = ONRTNQUOTE;
	if (pQuote)
	{
		CThostFtdcQuoteField *task_data = new CThostFtdcQuoteField();
		*task_data = *pQuote;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnQuoteInsert(CThostFtdcInputQuoteField *pInputQuote, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNQUOTEINSERT;
	if (pInputQuote)
	{
		CThostFtdcInputQuoteField *task_data = new CThostFtdcInputQuoteField();
		*task_data = *pInputQuote;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnQuoteAction(CThostFtdcQuoteActionField *pQuoteAction, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNQUOTEACTION;
	if (pQuoteAction)
	{
		CThostFtdcQuoteActionField *task_data = new CThostFtdcQuoteActionField();
		*task_data = *pQuoteAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnForQuoteRsp(CThostFtdcForQuoteRspField *pForQuoteRsp)
{
	Task task = Task();
	task.task_name = ONRTNFORQUOTERSP;
	if (pForQuoteRsp)
	{
		CThostFtdcForQuoteRspField *task_data = new CThostFtdcForQuoteRspField();
		*task_data = *pForQuoteRsp;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnCFMMCTradingAccountToken(CThostFtdcCFMMCTradingAccountTokenField *pCFMMCTradingAccountToken)
{
	Task task = Task();
	task.task_name = ONRTNCFMMCTRADINGACCOUNTTOKEN;
	if (pCFMMCTradingAccountToken)
	{
		CThostFtdcCFMMCTradingAccountTokenField *task_data = new CThostFtdcCFMMCTradingAccountTokenField();
		*task_data = *pCFMMCTradingAccountToken;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnBatchOrderAction(CThostFtdcBatchOrderActionField *pBatchOrderAction, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNBATCHORDERACTION;
	if (pBatchOrderAction)
	{
		CThostFtdcBatchOrderActionField *task_data = new CThostFtdcBatchOrderActionField();
		*task_data = *pBatchOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnOptionSelfClose(CThostFtdcOptionSelfCloseField *pOptionSelfClose)
{
	Task task = Task();
	task.task_name = ONRTNOPTIONSELFCLOSE;
	if (pOptionSelfClose)
	{
		CThostFtdcOptionSelfCloseField *task_data = new CThostFtdcOptionSelfCloseField();
		*task_data = *pOptionSelfClose;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnOptionSelfCloseInsert(CThostFtdcInputOptionSelfCloseField *pInputOptionSelfClose, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNOPTIONSELFCLOSEINSERT;
	if (pInputOptionSelfClose)
	{
		CThostFtdcInputOptionSelfCloseField *task_data = new CThostFtdcInputOptionSelfCloseField();
		*task_data = *pInputOptionSelfClose;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnOptionSelfCloseAction(CThostFtdcOptionSelfCloseActionField *pOptionSelfCloseAction, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNOPTIONSELFCLOSEACTION;
	if (pOptionSelfCloseAction)
	{
		CThostFtdcOptionSelfCloseActionField *task_data = new CThostFtdcOptionSelfCloseActionField();
		*task_data = *pOptionSelfCloseAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnCombAction(CThostFtdcCombActionField *pCombAction)
{
	Task task = Task();
	task.task_name = ONRTNCOMBACTION;
	if (pCombAction)
	{
		CThostFtdcCombActionField *task_data = new CThostFtdcCombActionField();
		*task_data = *pCombAction;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnCombActionInsert(CThostFtdcInputCombActionField *pInputCombAction, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNCOMBACTIONINSERT;
	if (pInputCombAction)
	{
		CThostFtdcInputCombActionField *task_data = new CThostFtdcInputCombActionField();
		*task_data = *pInputCombAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryContractBank(CThostFtdcContractBankField *pContractBank, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYCONTRACTBANK;
	if (pContractBank)
	{
		CThostFtdcContractBankField *task_data = new CThostFtdcContractBankField();
		*task_data = *pContractBank;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryParkedOrder(CThostFtdcParkedOrderField *pParkedOrder, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYPARKEDORDER;
	if (pParkedOrder)
	{
		CThostFtdcParkedOrderField *task_data = new CThostFtdcParkedOrderField();
		*task_data = *pParkedOrder;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryParkedOrderAction(CThostFtdcParkedOrderActionField *pParkedOrderAction, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYPARKEDORDERACTION;
	if (pParkedOrderAction)
	{
		CThostFtdcParkedOrderActionField *task_data = new CThostFtdcParkedOrderActionField();
		*task_data = *pParkedOrderAction;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryTradingNotice(CThostFtdcTradingNoticeField *pTradingNotice, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYTRADINGNOTICE;
	if (pTradingNotice)
	{
		CThostFtdcTradingNoticeField *task_data = new CThostFtdcTradingNoticeField();
		*task_data = *pTradingNotice;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryBrokerTradingParams(CThostFtdcBrokerTradingParamsField *pBrokerTradingParams, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYBROKERTRADINGPARAMS;
	if (pBrokerTradingParams)
	{
		CThostFtdcBrokerTradingParamsField *task_data = new CThostFtdcBrokerTradingParamsField();
		*task_data = *pBrokerTradingParams;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQryBrokerTradingAlgos(CThostFtdcBrokerTradingAlgosField *pBrokerTradingAlgos, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQRYBROKERTRADINGALGOS;
	if (pBrokerTradingAlgos)
	{
		CThostFtdcBrokerTradingAlgosField *task_data = new CThostFtdcBrokerTradingAlgosField();
		*task_data = *pBrokerTradingAlgos;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQueryCFMMCTradingAccountToken(CThostFtdcQueryCFMMCTradingAccountTokenField *pQueryCFMMCTradingAccountToken, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQUERYCFMMCTRADINGACCOUNTTOKEN;
	if (pQueryCFMMCTradingAccountToken)
	{
		CThostFtdcQueryCFMMCTradingAccountTokenField *task_data = new CThostFtdcQueryCFMMCTradingAccountTokenField();
		*task_data = *pQueryCFMMCTradingAccountToken;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRtnFromBankToFutureByBank(CThostFtdcRspTransferField *pRspTransfer)
{
	Task task = Task();
	task.task_name = ONRTNFROMBANKTOFUTUREBYBANK;
	if (pRspTransfer)
	{
		CThostFtdcRspTransferField *task_data = new CThostFtdcRspTransferField();
		*task_data = *pRspTransfer;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnFromFutureToBankByBank(CThostFtdcRspTransferField *pRspTransfer)
{
	Task task = Task();
	task.task_name = ONRTNFROMFUTURETOBANKBYBANK;
	if (pRspTransfer)
	{
		CThostFtdcRspTransferField *task_data = new CThostFtdcRspTransferField();
		*task_data = *pRspTransfer;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnRepealFromBankToFutureByBank(CThostFtdcRspRepealField *pRspRepeal)
{
	Task task = Task();
	task.task_name = ONRTNREPEALFROMBANKTOFUTUREBYBANK;
	if (pRspRepeal)
	{
		CThostFtdcRspRepealField *task_data = new CThostFtdcRspRepealField();
		*task_data = *pRspRepeal;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnRepealFromFutureToBankByBank(CThostFtdcRspRepealField *pRspRepeal)
{
	Task task = Task();
	task.task_name = ONRTNREPEALFROMFUTURETOBANKBYBANK;
	if (pRspRepeal)
	{
		CThostFtdcRspRepealField *task_data = new CThostFtdcRspRepealField();
		*task_data = *pRspRepeal;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnFromBankToFutureByFuture(CThostFtdcRspTransferField *pRspTransfer)
{
	Task task = Task();
	task.task_name = ONRTNFROMBANKTOFUTUREBYFUTURE;
	if (pRspTransfer)
	{
		CThostFtdcRspTransferField *task_data = new CThostFtdcRspTransferField();
		*task_data = *pRspTransfer;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnFromFutureToBankByFuture(CThostFtdcRspTransferField *pRspTransfer)
{
	Task task = Task();
	task.task_name = ONRTNFROMFUTURETOBANKBYFUTURE;
	if (pRspTransfer)
	{
		CThostFtdcRspTransferField *task_data = new CThostFtdcRspTransferField();
		*task_data = *pRspTransfer;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnRepealFromBankToFutureByFutureManual(CThostFtdcRspRepealField *pRspRepeal)
{
	Task task = Task();
	task.task_name = ONRTNREPEALFROMBANKTOFUTUREBYFUTUREMANUAL;
	if (pRspRepeal)
	{
		CThostFtdcRspRepealField *task_data = new CThostFtdcRspRepealField();
		*task_data = *pRspRepeal;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnRepealFromFutureToBankByFutureManual(CThostFtdcRspRepealField *pRspRepeal)
{
	Task task = Task();
	task.task_name = ONRTNREPEALFROMFUTURETOBANKBYFUTUREMANUAL;
	if (pRspRepeal)
	{
		CThostFtdcRspRepealField *task_data = new CThostFtdcRspRepealField();
		*task_data = *pRspRepeal;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnQueryBankBalanceByFuture(CThostFtdcNotifyQueryAccountField *pNotifyQueryAccount)
{
	Task task = Task();
	task.task_name = ONRTNQUERYBANKBALANCEBYFUTURE;
	if (pNotifyQueryAccount)
	{
		CThostFtdcNotifyQueryAccountField *task_data = new CThostFtdcNotifyQueryAccountField();
		*task_data = *pNotifyQueryAccount;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnBankToFutureByFuture(CThostFtdcReqTransferField *pReqTransfer, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNBANKTOFUTUREBYFUTURE;
	if (pReqTransfer)
	{
		CThostFtdcReqTransferField *task_data = new CThostFtdcReqTransferField();
		*task_data = *pReqTransfer;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnFutureToBankByFuture(CThostFtdcReqTransferField *pReqTransfer, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNFUTURETOBANKBYFUTURE;
	if (pReqTransfer)
	{
		CThostFtdcReqTransferField *task_data = new CThostFtdcReqTransferField();
		*task_data = *pReqTransfer;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnRepealBankToFutureByFutureManual(CThostFtdcReqRepealField *pReqRepeal, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNREPEALBANKTOFUTUREBYFUTUREMANUAL;
	if (pReqRepeal)
	{
		CThostFtdcReqRepealField *task_data = new CThostFtdcReqRepealField();
		*task_data = *pReqRepeal;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnRepealFutureToBankByFutureManual(CThostFtdcReqRepealField *pReqRepeal, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNREPEALFUTURETOBANKBYFUTUREMANUAL;
	if (pReqRepeal)
	{
		CThostFtdcReqRepealField *task_data = new CThostFtdcReqRepealField();
		*task_data = *pReqRepeal;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnErrRtnQueryBankBalanceByFuture(CThostFtdcReqQueryAccountField *pReqQueryAccount, CThostFtdcRspInfoField *pRspInfo)
{
	Task task = Task();
	task.task_name = ONERRRTNQUERYBANKBALANCEBYFUTURE;
	if (pReqQueryAccount)
	{
		CThostFtdcReqQueryAccountField *task_data = new CThostFtdcReqQueryAccountField();
		*task_data = *pReqQueryAccount;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnRepealFromBankToFutureByFuture(CThostFtdcRspRepealField *pRspRepeal)
{
	Task task = Task();
	task.task_name = ONRTNREPEALFROMBANKTOFUTUREBYFUTURE;
	if (pRspRepeal)
	{
		CThostFtdcRspRepealField *task_data = new CThostFtdcRspRepealField();
		*task_data = *pRspRepeal;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnRepealFromFutureToBankByFuture(CThostFtdcRspRepealField *pRspRepeal)
{
	Task task = Task();
	task.task_name = ONRTNREPEALFROMFUTURETOBANKBYFUTURE;
	if (pRspRepeal)
	{
		CThostFtdcRspRepealField *task_data = new CThostFtdcRspRepealField();
		*task_data = *pRspRepeal;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRspFromBankToFutureByFuture(CThostFtdcReqTransferField *pReqTransfer, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPFROMBANKTOFUTUREBYFUTURE;
	if (pReqTransfer)
	{
		CThostFtdcReqTransferField *task_data = new CThostFtdcReqTransferField();
		*task_data = *pReqTransfer;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspFromFutureToBankByFuture(CThostFtdcReqTransferField *pReqTransfer, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPFROMFUTURETOBANKBYFUTURE;
	if (pReqTransfer)
	{
		CThostFtdcReqTransferField *task_data = new CThostFtdcReqTransferField();
		*task_data = *pReqTransfer;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRspQueryBankAccountMoneyByFuture(CThostFtdcReqQueryAccountField *pReqQueryAccount, CThostFtdcRspInfoField *pRspInfo, int nRequestID, bool bIsLast)
{
	Task task = Task();
	task.task_name = ONRSPQUERYBANKACCOUNTMONEYBYFUTURE;
	if (pReqQueryAccount)
	{
		CThostFtdcReqQueryAccountField *task_data = new CThostFtdcReqQueryAccountField();
		*task_data = *pReqQueryAccount;
		task.task_data = task_data;
	}
	if (pRspInfo)
	{
		CThostFtdcRspInfoField *task_error = new CThostFtdcRspInfoField();
		*task_error = *pRspInfo;
		task.task_error = task_error;
	}
	task.task_id = nRequestID;
	task.task_last = bIsLast;
	this->task_queue.push(task);
};

void TdApiApp::OnRtnOpenAccountByBank(CThostFtdcOpenAccountField *pOpenAccount)
{
	Task task = Task();
	task.task_name = ONRTNOPENACCOUNTBYBANK;
	if (pOpenAccount)
	{
		CThostFtdcOpenAccountField *task_data = new CThostFtdcOpenAccountField();
		*task_data = *pOpenAccount;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnCancelAccountByBank(CThostFtdcCancelAccountField *pCancelAccount)
{
	Task task = Task();
	task.task_name = ONRTNCANCELACCOUNTBYBANK;
	if (pCancelAccount)
	{
		CThostFtdcCancelAccountField *task_data = new CThostFtdcCancelAccountField();
		*task_data = *pCancelAccount;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};

void TdApiApp::OnRtnChangeAccountByBank(CThostFtdcChangeAccountField *pChangeAccount)
{
	Task task = Task();
	task.task_name = ONRTNCHANGEACCOUNTBYBANK;
	if (pChangeAccount)
	{
		CThostFtdcChangeAccountField *task_data = new CThostFtdcChangeAccountField();
		*task_data = *pChangeAccount;
		task.task_data = task_data;
	}
	this->task_queue.push(task);
};


///-------------------------------------------------------------------------------------
///工作线程从队列中取出数据，转化为python对象后，进行推送
///-------------------------------------------------------------------------------------

void TdApiApp::processTask()
{
    try
    {
        while (this->active)
        {
            Task task = this->task_queue.pop();

            switch (task.task_name)
            {
			case ONFRONTCONNECTED:
			{
				this->processFrontConnected(&task);
				break;
			}

			case ONFRONTDISCONNECTED:
			{
				this->processFrontDisconnected(&task);
				break;
			}

			case ONHEARTBEATWARNING:
			{
				this->processHeartBeatWarning(&task);
				break;
			}

			case ONRSPAUTHENTICATE:
			{
				this->processRspAuthenticate(&task);
				break;
			}

			case ONRSPUSERLOGIN:
			{
				this->processRspUserLogin(&task);
				break;
			}

			case ONRSPUSERLOGOUT:
			{
				this->processRspUserLogout(&task);
				break;
			}

			case ONRSPUSERPASSWORDUPDATE:
			{
				this->processRspUserPasswordUpdate(&task);
				break;
			}

			case ONRSPTRADINGACCOUNTPASSWORDUPDATE:
			{
				this->processRspTradingAccountPasswordUpdate(&task);
				break;
			}

			case ONRSPUSERAUTHMETHOD:
			{
				this->processRspUserAuthMethod(&task);
				break;
			}

			case ONRSPGENUSERCAPTCHA:
			{
				this->processRspGenUserCaptcha(&task);
				break;
			}

			case ONRSPGENUSERTEXT:
			{
				this->processRspGenUserText(&task);
				break;
			}

			case ONRSPORDERINSERT:
			{
				this->processRspOrderInsert(&task);
				break;
			}

			case ONRSPPARKEDORDERINSERT:
			{
				this->processRspParkedOrderInsert(&task);
				break;
			}

			case ONRSPPARKEDORDERACTION:
			{
				this->processRspParkedOrderAction(&task);
				break;
			}

			case ONRSPORDERACTION:
			{
				this->processRspOrderAction(&task);
				break;
			}

			case ONRSPQUERYMAXORDERVOLUME:
			{
				this->processRspQueryMaxOrderVolume(&task);
				break;
			}

			case ONRSPSETTLEMENTINFOCONFIRM:
			{
				this->processRspSettlementInfoConfirm(&task);
				break;
			}

			case ONRSPREMOVEPARKEDORDER:
			{
				this->processRspRemoveParkedOrder(&task);
				break;
			}

			case ONRSPREMOVEPARKEDORDERACTION:
			{
				this->processRspRemoveParkedOrderAction(&task);
				break;
			}

			case ONRSPEXECORDERINSERT:
			{
				this->processRspExecOrderInsert(&task);
				break;
			}

			case ONRSPEXECORDERACTION:
			{
				this->processRspExecOrderAction(&task);
				break;
			}

			case ONRSPFORQUOTEINSERT:
			{
				this->processRspForQuoteInsert(&task);
				break;
			}

			case ONRSPQUOTEINSERT:
			{
				this->processRspQuoteInsert(&task);
				break;
			}

			case ONRSPQUOTEACTION:
			{
				this->processRspQuoteAction(&task);
				break;
			}

			case ONRSPBATCHORDERACTION:
			{
				this->processRspBatchOrderAction(&task);
				break;
			}

			case ONRSPOPTIONSELFCLOSEINSERT:
			{
				this->processRspOptionSelfCloseInsert(&task);
				break;
			}

			case ONRSPOPTIONSELFCLOSEACTION:
			{
				this->processRspOptionSelfCloseAction(&task);
				break;
			}

			case ONRSPCOMBACTIONINSERT:
			{
				this->processRspCombActionInsert(&task);
				break;
			}

			case ONRSPQRYORDER:
			{
				this->processRspQryOrder(&task);
				break;
			}

			case ONRSPQRYTRADE:
			{
				this->processRspQryTrade(&task);
				break;
			}

			case ONRSPQRYINVESTORPOSITION:
			{
				this->processRspQryInvestorPosition(&task);
				break;
			}

			case ONRSPQRYTRADINGACCOUNT:
			{
				this->processRspQryTradingAccount(&task);
				break;
			}

			case ONRSPQRYINVESTOR:
			{
				this->processRspQryInvestor(&task);
				break;
			}

			case ONRSPQRYTRADINGCODE:
			{
				this->processRspQryTradingCode(&task);
				break;
			}

			case ONRSPQRYINSTRUMENTMARGINRATE:
			{
				this->processRspQryInstrumentMarginRate(&task);
				break;
			}

			case ONRSPQRYINSTRUMENTCOMMISSIONRATE:
			{
				this->processRspQryInstrumentCommissionRate(&task);
				break;
			}

			case ONRSPQRYEXCHANGE:
			{
				this->processRspQryExchange(&task);
				break;
			}

			case ONRSPQRYPRODUCT:
			{
				this->processRspQryProduct(&task);
				break;
			}

			case ONRSPQRYINSTRUMENT:
			{
				this->processRspQryInstrument(&task);
				break;
			}

			case ONRSPQRYDEPTHMARKETDATA:
			{
				this->processRspQryDepthMarketData(&task);
				break;
			}

			case ONRSPQRYSETTLEMENTINFO:
			{
				this->processRspQrySettlementInfo(&task);
				break;
			}

			case ONRSPQRYTRANSFERBANK:
			{
				this->processRspQryTransferBank(&task);
				break;
			}

			case ONRSPQRYINVESTORPOSITIONDETAIL:
			{
				this->processRspQryInvestorPositionDetail(&task);
				break;
			}

			case ONRSPQRYNOTICE:
			{
				this->processRspQryNotice(&task);
				break;
			}

			case ONRSPQRYSETTLEMENTINFOCONFIRM:
			{
				this->processRspQrySettlementInfoConfirm(&task);
				break;
			}

			case ONRSPQRYINVESTORPOSITIONCOMBINEDETAIL:
			{
				this->processRspQryInvestorPositionCombineDetail(&task);
				break;
			}

			case ONRSPQRYCFMMCTRADINGACCOUNTKEY:
			{
				this->processRspQryCFMMCTradingAccountKey(&task);
				break;
			}

			case ONRSPQRYEWARRANTOFFSET:
			{
				this->processRspQryEWarrantOffset(&task);
				break;
			}

			case ONRSPQRYINVESTORPRODUCTGROUPMARGIN:
			{
				this->processRspQryInvestorProductGroupMargin(&task);
				break;
			}

			case ONRSPQRYEXCHANGEMARGINRATE:
			{
				this->processRspQryExchangeMarginRate(&task);
				break;
			}

			case ONRSPQRYEXCHANGEMARGINRATEADJUST:
			{
				this->processRspQryExchangeMarginRateAdjust(&task);
				break;
			}

			case ONRSPQRYEXCHANGERATE:
			{
				this->processRspQryExchangeRate(&task);
				break;
			}

			case ONRSPQRYSECAGENTACIDMAP:
			{
				this->processRspQrySecAgentACIDMap(&task);
				break;
			}

			case ONRSPQRYPRODUCTEXCHRATE:
			{
				this->processRspQryProductExchRate(&task);
				break;
			}

			case ONRSPQRYPRODUCTGROUP:
			{
				this->processRspQryProductGroup(&task);
				break;
			}

			case ONRSPQRYMMINSTRUMENTCOMMISSIONRATE:
			{
				this->processRspQryMMInstrumentCommissionRate(&task);
				break;
			}

			case ONRSPQRYMMOPTIONINSTRCOMMRATE:
			{
				this->processRspQryMMOptionInstrCommRate(&task);
				break;
			}

			case ONRSPQRYINSTRUMENTORDERCOMMRATE:
			{
				this->processRspQryInstrumentOrderCommRate(&task);
				break;
			}

			case ONRSPQRYSECAGENTTRADINGACCOUNT:
			{
				this->processRspQrySecAgentTradingAccount(&task);
				break;
			}

			case ONRSPQRYSECAGENTCHECKMODE:
			{
				this->processRspQrySecAgentCheckMode(&task);
				break;
			}

			case ONRSPQRYSECAGENTTRADEINFO:
			{
				this->processRspQrySecAgentTradeInfo(&task);
				break;
			}

			case ONRSPQRYOPTIONINSTRTRADECOST:
			{
				this->processRspQryOptionInstrTradeCost(&task);
				break;
			}

			case ONRSPQRYOPTIONINSTRCOMMRATE:
			{
				this->processRspQryOptionInstrCommRate(&task);
				break;
			}

			case ONRSPQRYEXECORDER:
			{
				this->processRspQryExecOrder(&task);
				break;
			}

			case ONRSPQRYFORQUOTE:
			{
				this->processRspQryForQuote(&task);
				break;
			}

			case ONRSPQRYQUOTE:
			{
				this->processRspQryQuote(&task);
				break;
			}

			case ONRSPQRYOPTIONSELFCLOSE:
			{
				this->processRspQryOptionSelfClose(&task);
				break;
			}

			case ONRSPQRYINVESTUNIT:
			{
				this->processRspQryInvestUnit(&task);
				break;
			}

			case ONRSPQRYCOMBINSTRUMENTGUARD:
			{
				this->processRspQryCombInstrumentGuard(&task);
				break;
			}

			case ONRSPQRYCOMBACTION:
			{
				this->processRspQryCombAction(&task);
				break;
			}

			case ONRSPQRYTRANSFERSERIAL:
			{
				this->processRspQryTransferSerial(&task);
				break;
			}

			case ONRSPQRYACCOUNTREGISTER:
			{
				this->processRspQryAccountregister(&task);
				break;
			}

			case ONRSPERROR:
			{
				this->processRspError(&task);
				break;
			}

			case ONRTNORDER:
			{
				this->processRtnOrder(&task);
				break;
			}

			case ONRTNTRADE:
			{
				this->processRtnTrade(&task);
				break;
			}

			case ONERRRTNORDERINSERT:
			{
				this->processErrRtnOrderInsert(&task);
				break;
			}

			case ONERRRTNORDERACTION:
			{
				this->processErrRtnOrderAction(&task);
				break;
			}

			case ONRTNINSTRUMENTSTATUS:
			{
				this->processRtnInstrumentStatus(&task);
				break;
			}

			case ONRTNBULLETIN:
			{
				this->processRtnBulletin(&task);
				break;
			}

			case ONRTNTRADINGNOTICE:
			{
				this->processRtnTradingNotice(&task);
				break;
			}

			case ONRTNERRORCONDITIONALORDER:
			{
				this->processRtnErrorConditionalOrder(&task);
				break;
			}

			case ONRTNEXECORDER:
			{
				this->processRtnExecOrder(&task);
				break;
			}

			case ONERRRTNEXECORDERINSERT:
			{
				this->processErrRtnExecOrderInsert(&task);
				break;
			}

			case ONERRRTNEXECORDERACTION:
			{
				this->processErrRtnExecOrderAction(&task);
				break;
			}

			case ONERRRTNFORQUOTEINSERT:
			{
				this->processErrRtnForQuoteInsert(&task);
				break;
			}

			case ONRTNQUOTE:
			{
				this->processRtnQuote(&task);
				break;
			}

			case ONERRRTNQUOTEINSERT:
			{
				this->processErrRtnQuoteInsert(&task);
				break;
			}

			case ONERRRTNQUOTEACTION:
			{
				this->processErrRtnQuoteAction(&task);
				break;
			}

			case ONRTNFORQUOTERSP:
			{
				this->processRtnForQuoteRsp(&task);
				break;
			}

			case ONRTNCFMMCTRADINGACCOUNTTOKEN:
			{
				this->processRtnCFMMCTradingAccountToken(&task);
				break;
			}

			case ONERRRTNBATCHORDERACTION:
			{
				this->processErrRtnBatchOrderAction(&task);
				break;
			}

			case ONRTNOPTIONSELFCLOSE:
			{
				this->processRtnOptionSelfClose(&task);
				break;
			}

			case ONERRRTNOPTIONSELFCLOSEINSERT:
			{
				this->processErrRtnOptionSelfCloseInsert(&task);
				break;
			}

			case ONERRRTNOPTIONSELFCLOSEACTION:
			{
				this->processErrRtnOptionSelfCloseAction(&task);
				break;
			}

			case ONRTNCOMBACTION:
			{
				this->processRtnCombAction(&task);
				break;
			}

			case ONERRRTNCOMBACTIONINSERT:
			{
				this->processErrRtnCombActionInsert(&task);
				break;
			}

			case ONRSPQRYCONTRACTBANK:
			{
				this->processRspQryContractBank(&task);
				break;
			}

			case ONRSPQRYPARKEDORDER:
			{
				this->processRspQryParkedOrder(&task);
				break;
			}

			case ONRSPQRYPARKEDORDERACTION:
			{
				this->processRspQryParkedOrderAction(&task);
				break;
			}

			case ONRSPQRYTRADINGNOTICE:
			{
				this->processRspQryTradingNotice(&task);
				break;
			}

			case ONRSPQRYBROKERTRADINGPARAMS:
			{
				this->processRspQryBrokerTradingParams(&task);
				break;
			}

			case ONRSPQRYBROKERTRADINGALGOS:
			{
				this->processRspQryBrokerTradingAlgos(&task);
				break;
			}

			case ONRSPQUERYCFMMCTRADINGACCOUNTTOKEN:
			{
				this->processRspQueryCFMMCTradingAccountToken(&task);
				break;
			}

			case ONRTNFROMBANKTOFUTUREBYBANK:
			{
				this->processRtnFromBankToFutureByBank(&task);
				break;
			}

			case ONRTNFROMFUTURETOBANKBYBANK:
			{
				this->processRtnFromFutureToBankByBank(&task);
				break;
			}

			case ONRTNREPEALFROMBANKTOFUTUREBYBANK:
			{
				this->processRtnRepealFromBankToFutureByBank(&task);
				break;
			}

			case ONRTNREPEALFROMFUTURETOBANKBYBANK:
			{
				this->processRtnRepealFromFutureToBankByBank(&task);
				break;
			}

			case ONRTNFROMBANKTOFUTUREBYFUTURE:
			{
				this->processRtnFromBankToFutureByFuture(&task);
				break;
			}

			case ONRTNFROMFUTURETOBANKBYFUTURE:
			{
				this->processRtnFromFutureToBankByFuture(&task);
				break;
			}

			case ONRTNREPEALFROMBANKTOFUTUREBYFUTUREMANUAL:
			{
				this->processRtnRepealFromBankToFutureByFutureManual(&task);
				break;
			}

			case ONRTNREPEALFROMFUTURETOBANKBYFUTUREMANUAL:
			{
				this->processRtnRepealFromFutureToBankByFutureManual(&task);
				break;
			}

			case ONRTNQUERYBANKBALANCEBYFUTURE:
			{
				this->processRtnQueryBankBalanceByFuture(&task);
				break;
			}

			case ONERRRTNBANKTOFUTUREBYFUTURE:
			{
				this->processErrRtnBankToFutureByFuture(&task);
				break;
			}

			case ONERRRTNFUTURETOBANKBYFUTURE:
			{
				this->processErrRtnFutureToBankByFuture(&task);
				break;
			}

			case ONERRRTNREPEALBANKTOFUTUREBYFUTUREMANUAL:
			{
				this->processErrRtnRepealBankToFutureByFutureManual(&task);
				break;
			}

			case ONERRRTNREPEALFUTURETOBANKBYFUTUREMANUAL:
			{
				this->processErrRtnRepealFutureToBankByFutureManual(&task);
				break;
			}

			case ONERRRTNQUERYBANKBALANCEBYFUTURE:
			{
				this->processErrRtnQueryBankBalanceByFuture(&task);
				break;
			}

			case ONRTNREPEALFROMBANKTOFUTUREBYFUTURE:
			{
				this->processRtnRepealFromBankToFutureByFuture(&task);
				break;
			}

			case ONRTNREPEALFROMFUTURETOBANKBYFUTURE:
			{
				this->processRtnRepealFromFutureToBankByFuture(&task);
				break;
			}

			case ONRSPFROMBANKTOFUTUREBYFUTURE:
			{
				this->processRspFromBankToFutureByFuture(&task);
				break;
			}

			case ONRSPFROMFUTURETOBANKBYFUTURE:
			{
				this->processRspFromFutureToBankByFuture(&task);
				break;
			}

			case ONRSPQUERYBANKACCOUNTMONEYBYFUTURE:
			{
				this->processRspQueryBankAccountMoneyByFuture(&task);
				break;
			}

			case ONRTNOPENACCOUNTBYBANK:
			{
				this->processRtnOpenAccountByBank(&task);
				break;
			}

			case ONRTNCANCELACCOUNTBYBANK:
			{
				this->processRtnCancelAccountByBank(&task);
				break;
			}

			case ONRTNCHANGEACCOUNTBYBANK:
			{
				this->processRtnChangeAccountByBank(&task);
				break;
			}
            };
        }
    }
    catch (const TerminatedError&)
    {
    }
};

void TdApiApp::processFrontConnected(Task *task)
{
	gil_scoped_acquire acquire;
	this->onFrontConnected();
};

void TdApiApp::processFrontDisconnected(Task *task)
{
	gil_scoped_acquire acquire;
	this->onFrontDisconnected(task->task_id);
};

void TdApiApp::processHeartBeatWarning(Task *task)
{
	gil_scoped_acquire acquire;
	this->onHeartBeatWarning(task->task_id);
};

void TdApiApp::processRspAuthenticate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspAuthenticateField *task_data = (CThostFtdcRspAuthenticateField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["UserID"] = toUtf(task_data->UserID);
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["AppID"] = toUtf(task_data->AppID);
		data["AppType"] = task_data->AppType;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspAuthenticate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspUserLogin(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspUserLoginField *task_data = (CThostFtdcRspUserLoginField*)task->task_data;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["LoginTime"] = toUtf(task_data->LoginTime);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["UserID"] = toUtf(task_data->UserID);
		data["SystemName"] = toUtf(task_data->SystemName);
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["MaxOrderRef"] = toUtf(task_data->MaxOrderRef);
		data["SHFETime"] = toUtf(task_data->SHFETime);
		data["DCETime"] = toUtf(task_data->DCETime);
		data["CZCETime"] = toUtf(task_data->CZCETime);
		data["FFEXTime"] = toUtf(task_data->FFEXTime);
		data["INETime"] = toUtf(task_data->INETime);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspUserLogin(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspUserLogout(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcUserLogoutField *task_data = (CThostFtdcUserLogoutField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["UserID"] = toUtf(task_data->UserID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspUserLogout(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspUserPasswordUpdate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcUserPasswordUpdateField *task_data = (CThostFtdcUserPasswordUpdateField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["UserID"] = toUtf(task_data->UserID);
		data["OldPassword"] = toUtf(task_data->OldPassword);
		data["NewPassword"] = toUtf(task_data->NewPassword);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspUserPasswordUpdate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspTradingAccountPasswordUpdate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradingAccountPasswordUpdateField *task_data = (CThostFtdcTradingAccountPasswordUpdateField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["OldPassword"] = toUtf(task_data->OldPassword);
		data["NewPassword"] = toUtf(task_data->NewPassword);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspTradingAccountPasswordUpdate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspUserAuthMethod(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspUserAuthMethodField *task_data = (CThostFtdcRspUserAuthMethodField*)task->task_data;
		data["UsableAuthMethod"] = task_data->UsableAuthMethod;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspUserAuthMethod(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspGenUserCaptcha(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspGenUserCaptchaField *task_data = (CThostFtdcRspGenUserCaptchaField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["UserID"] = toUtf(task_data->UserID);
		data["CaptchaInfoLen"] = task_data->CaptchaInfoLen;
		data["CaptchaInfo"] = toUtf(task_data->CaptchaInfo);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspGenUserCaptcha(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspGenUserText(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspGenUserTextField *task_data = (CThostFtdcRspGenUserTextField*)task->task_data;
		data["UserTextSeq"] = task_data->UserTextSeq;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspGenUserText(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspOrderInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputOrderField *task_data = (CThostFtdcInputOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["UserForceClose"] = task_data->UserForceClose;
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspOrderInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspParkedOrderInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcParkedOrderField *task_data = (CThostFtdcParkedOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["UserForceClose"] = task_data->UserForceClose;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParkedOrderID"] = toUtf(task_data->ParkedOrderID);
		data["UserType"] = task_data->UserType;
		data["Status"] = task_data->Status;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspParkedOrderInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspParkedOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcParkedOrderActionField *task_data = (CThostFtdcParkedOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OrderActionRef"] = task_data->OrderActionRef;
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeChange"] = task_data->VolumeChange;
		data["UserID"] = toUtf(task_data->UserID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ParkedOrderActionID"] = toUtf(task_data->ParkedOrderActionID);
		data["UserType"] = task_data->UserType;
		data["Status"] = task_data->Status;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspParkedOrderAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputOrderActionField *task_data = (CThostFtdcInputOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OrderActionRef"] = task_data->OrderActionRef;
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeChange"] = task_data->VolumeChange;
		data["UserID"] = toUtf(task_data->UserID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspOrderAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQueryMaxOrderVolume(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcQueryMaxOrderVolumeField *task_data = (CThostFtdcQueryMaxOrderVolumeField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["Direction"] = task_data->Direction;
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["MaxVolume"] = task_data->MaxVolume;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQueryMaxOrderVolume(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspSettlementInfoConfirm(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcSettlementInfoConfirmField *task_data = (CThostFtdcSettlementInfoConfirmField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ConfirmDate"] = toUtf(task_data->ConfirmDate);
		data["ConfirmTime"] = toUtf(task_data->ConfirmTime);
		data["SettlementID"] = task_data->SettlementID;
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspSettlementInfoConfirm(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspRemoveParkedOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRemoveParkedOrderField *task_data = (CThostFtdcRemoveParkedOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ParkedOrderID"] = toUtf(task_data->ParkedOrderID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspRemoveParkedOrder(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspRemoveParkedOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRemoveParkedOrderActionField *task_data = (CThostFtdcRemoveParkedOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ParkedOrderActionID"] = toUtf(task_data->ParkedOrderActionID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspRemoveParkedOrderAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspExecOrderInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputExecOrderField *task_data = (CThostFtdcInputExecOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ExecOrderRef"] = toUtf(task_data->ExecOrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ActionType"] = task_data->ActionType;
		data["PosiDirection"] = task_data->PosiDirection;
		data["ReservePositionFlag"] = task_data->ReservePositionFlag;
		data["CloseFlag"] = task_data->CloseFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspExecOrderInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspExecOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputExecOrderActionField *task_data = (CThostFtdcInputExecOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ExecOrderActionRef"] = task_data->ExecOrderActionRef;
		data["ExecOrderRef"] = toUtf(task_data->ExecOrderRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ExecOrderSysID"] = toUtf(task_data->ExecOrderSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["UserID"] = toUtf(task_data->UserID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspExecOrderAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspForQuoteInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputForQuoteField *task_data = (CThostFtdcInputForQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ForQuoteRef"] = toUtf(task_data->ForQuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspForQuoteInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQuoteInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputQuoteField *task_data = (CThostFtdcInputQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["QuoteRef"] = toUtf(task_data->QuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["AskPrice"] = task_data->AskPrice;
		data["BidPrice"] = task_data->BidPrice;
		data["AskVolume"] = task_data->AskVolume;
		data["BidVolume"] = task_data->BidVolume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["AskOffsetFlag"] = task_data->AskOffsetFlag;
		data["BidOffsetFlag"] = task_data->BidOffsetFlag;
		data["AskHedgeFlag"] = task_data->AskHedgeFlag;
		data["BidHedgeFlag"] = task_data->BidHedgeFlag;
		data["AskOrderRef"] = toUtf(task_data->AskOrderRef);
		data["BidOrderRef"] = toUtf(task_data->BidOrderRef);
		data["ForQuoteSysID"] = toUtf(task_data->ForQuoteSysID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQuoteInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQuoteAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputQuoteActionField *task_data = (CThostFtdcInputQuoteActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["QuoteActionRef"] = task_data->QuoteActionRef;
		data["QuoteRef"] = toUtf(task_data->QuoteRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["QuoteSysID"] = toUtf(task_data->QuoteSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["UserID"] = toUtf(task_data->UserID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQuoteAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspBatchOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputBatchOrderActionField *task_data = (CThostFtdcInputBatchOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OrderActionRef"] = task_data->OrderActionRef;
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["UserID"] = toUtf(task_data->UserID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspBatchOrderAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspOptionSelfCloseInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputOptionSelfCloseField *task_data = (CThostFtdcInputOptionSelfCloseField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OptionSelfCloseRef"] = toUtf(task_data->OptionSelfCloseRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["OptSelfCloseFlag"] = task_data->OptSelfCloseFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspOptionSelfCloseInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspOptionSelfCloseAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputOptionSelfCloseActionField *task_data = (CThostFtdcInputOptionSelfCloseActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OptionSelfCloseActionRef"] = task_data->OptionSelfCloseActionRef;
		data["OptionSelfCloseRef"] = toUtf(task_data->OptionSelfCloseRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["OptionSelfCloseSysID"] = toUtf(task_data->OptionSelfCloseSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["UserID"] = toUtf(task_data->UserID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspOptionSelfCloseAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspCombActionInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputCombActionField *task_data = (CThostFtdcInputCombActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["CombActionRef"] = toUtf(task_data->CombActionRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Direction"] = task_data->Direction;
		data["Volume"] = task_data->Volume;
		data["CombDirection"] = task_data->CombDirection;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspCombActionInsert(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOrderField *task_data = (CThostFtdcOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["OrderLocalID"] = toUtf(task_data->OrderLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["OrderSource"] = task_data->OrderSource;
		data["OrderStatus"] = task_data->OrderStatus;
		data["OrderType"] = task_data->OrderType;
		data["VolumeTraded"] = task_data->VolumeTraded;
		data["VolumeTotal"] = task_data->VolumeTotal;
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["ActiveTime"] = toUtf(task_data->ActiveTime);
		data["SuspendTime"] = toUtf(task_data->SuspendTime);
		data["UpdateTime"] = toUtf(task_data->UpdateTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ActiveTraderID"] = toUtf(task_data->ActiveTraderID);
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["UserForceClose"] = task_data->UserForceClose;
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerOrderSeq"] = task_data->BrokerOrderSeq;
		data["RelativeOrderSysID"] = toUtf(task_data->RelativeOrderSysID);
		data["ZCETotalTradedVolume"] = task_data->ZCETotalTradedVolume;
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryOrder(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryTrade(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradeField *task_data = (CThostFtdcTradeField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["TradeID"] = toUtf(task_data->TradeID);
		data["Direction"] = task_data->Direction;
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["TradingRole"] = task_data->TradingRole;
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["Price"] = task_data->Price;
		data["Volume"] = task_data->Volume;
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["TradeType"] = task_data->TradeType;
		data["PriceSource"] = task_data->PriceSource;
		data["TraderID"] = toUtf(task_data->TraderID);
		data["OrderLocalID"] = toUtf(task_data->OrderLocalID);
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["SequenceNo"] = task_data->SequenceNo;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["BrokerOrderSeq"] = task_data->BrokerOrderSeq;
		data["TradeSource"] = task_data->TradeSource;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryTrade(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInvestorPosition(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInvestorPositionField *task_data = (CThostFtdcInvestorPositionField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["PosiDirection"] = task_data->PosiDirection;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["PositionDate"] = task_data->PositionDate;
		data["YdPosition"] = task_data->YdPosition;
		data["Position"] = task_data->Position;
		data["LongFrozen"] = task_data->LongFrozen;
		data["ShortFrozen"] = task_data->ShortFrozen;
		data["LongFrozenAmount"] = task_data->LongFrozenAmount;
		data["ShortFrozenAmount"] = task_data->ShortFrozenAmount;
		data["OpenVolume"] = task_data->OpenVolume;
		data["CloseVolume"] = task_data->CloseVolume;
		data["OpenAmount"] = task_data->OpenAmount;
		data["CloseAmount"] = task_data->CloseAmount;
		data["PositionCost"] = task_data->PositionCost;
		data["PreMargin"] = task_data->PreMargin;
		data["UseMargin"] = task_data->UseMargin;
		data["FrozenMargin"] = task_data->FrozenMargin;
		data["FrozenCash"] = task_data->FrozenCash;
		data["FrozenCommission"] = task_data->FrozenCommission;
		data["CashIn"] = task_data->CashIn;
		data["Commission"] = task_data->Commission;
		data["CloseProfit"] = task_data->CloseProfit;
		data["PositionProfit"] = task_data->PositionProfit;
		data["PreSettlementPrice"] = task_data->PreSettlementPrice;
		data["SettlementPrice"] = task_data->SettlementPrice;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["OpenCost"] = task_data->OpenCost;
		data["ExchangeMargin"] = task_data->ExchangeMargin;
		data["CombPosition"] = task_data->CombPosition;
		data["CombLongFrozen"] = task_data->CombLongFrozen;
		data["CombShortFrozen"] = task_data->CombShortFrozen;
		data["CloseProfitByDate"] = task_data->CloseProfitByDate;
		data["CloseProfitByTrade"] = task_data->CloseProfitByTrade;
		data["TodayPosition"] = task_data->TodayPosition;
		data["MarginRateByMoney"] = task_data->MarginRateByMoney;
		data["MarginRateByVolume"] = task_data->MarginRateByVolume;
		data["StrikeFrozen"] = task_data->StrikeFrozen;
		data["StrikeFrozenAmount"] = task_data->StrikeFrozenAmount;
		data["AbandonFrozen"] = task_data->AbandonFrozen;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["YdStrikeFrozen"] = task_data->YdStrikeFrozen;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInvestorPosition(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryTradingAccount(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradingAccountField *task_data = (CThostFtdcTradingAccountField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["PreMortgage"] = task_data->PreMortgage;
		data["PreCredit"] = task_data->PreCredit;
		data["PreDeposit"] = task_data->PreDeposit;
		data["PreBalance"] = task_data->PreBalance;
		data["PreMargin"] = task_data->PreMargin;
		data["InterestBase"] = task_data->InterestBase;
		data["Interest"] = task_data->Interest;
		data["Deposit"] = task_data->Deposit;
		data["Withdraw"] = task_data->Withdraw;
		data["FrozenMargin"] = task_data->FrozenMargin;
		data["FrozenCash"] = task_data->FrozenCash;
		data["FrozenCommission"] = task_data->FrozenCommission;
		data["CurrMargin"] = task_data->CurrMargin;
		data["CashIn"] = task_data->CashIn;
		data["Commission"] = task_data->Commission;
		data["CloseProfit"] = task_data->CloseProfit;
		data["PositionProfit"] = task_data->PositionProfit;
		data["Balance"] = task_data->Balance;
		data["Available"] = task_data->Available;
		data["WithdrawQuota"] = task_data->WithdrawQuota;
		data["Reserve"] = task_data->Reserve;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["Credit"] = task_data->Credit;
		data["Mortgage"] = task_data->Mortgage;
		data["ExchangeMargin"] = task_data->ExchangeMargin;
		data["DeliveryMargin"] = task_data->DeliveryMargin;
		data["ExchangeDeliveryMargin"] = task_data->ExchangeDeliveryMargin;
		data["ReserveBalance"] = task_data->ReserveBalance;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["PreFundMortgageIn"] = task_data->PreFundMortgageIn;
		data["PreFundMortgageOut"] = task_data->PreFundMortgageOut;
		data["FundMortgageIn"] = task_data->FundMortgageIn;
		data["FundMortgageOut"] = task_data->FundMortgageOut;
		data["FundMortgageAvailable"] = task_data->FundMortgageAvailable;
		data["MortgageableFund"] = task_data->MortgageableFund;
		data["SpecProductMargin"] = task_data->SpecProductMargin;
		data["SpecProductFrozenMargin"] = task_data->SpecProductFrozenMargin;
		data["SpecProductCommission"] = task_data->SpecProductCommission;
		data["SpecProductFrozenCommission"] = task_data->SpecProductFrozenCommission;
		data["SpecProductPositionProfit"] = task_data->SpecProductPositionProfit;
		data["SpecProductCloseProfit"] = task_data->SpecProductCloseProfit;
		data["SpecProductPositionProfitByAlg"] = task_data->SpecProductPositionProfitByAlg;
		data["SpecProductExchangeMargin"] = task_data->SpecProductExchangeMargin;
		data["BizType"] = task_data->BizType;
		data["FrozenSwap"] = task_data->FrozenSwap;
		data["RemainSwap"] = task_data->RemainSwap;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryTradingAccount(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInvestor(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInvestorField *task_data = (CThostFtdcInvestorField*)task->task_data;
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorGroupID"] = toUtf(task_data->InvestorGroupID);
		data["InvestorName"] = toUtf(task_data->InvestorName);
		data["IdentifiedCardType"] = task_data->IdentifiedCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["IsActive"] = task_data->IsActive;
		data["Telephone"] = toUtf(task_data->Telephone);
		data["Address"] = toUtf(task_data->Address);
		data["OpenDate"] = toUtf(task_data->OpenDate);
		data["Mobile"] = toUtf(task_data->Mobile);
		data["CommModelID"] = toUtf(task_data->CommModelID);
		data["MarginModelID"] = toUtf(task_data->MarginModelID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInvestor(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryTradingCode(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradingCodeField *task_data = (CThostFtdcTradingCodeField*)task->task_data;
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IsActive"] = task_data->IsActive;
		data["ClientIDType"] = task_data->ClientIDType;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["BizType"] = task_data->BizType;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryTradingCode(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInstrumentMarginRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInstrumentMarginRateField *task_data = (CThostFtdcInstrumentMarginRateField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["LongMarginRatioByMoney"] = task_data->LongMarginRatioByMoney;
		data["LongMarginRatioByVolume"] = task_data->LongMarginRatioByVolume;
		data["ShortMarginRatioByMoney"] = task_data->ShortMarginRatioByMoney;
		data["ShortMarginRatioByVolume"] = task_data->ShortMarginRatioByVolume;
		data["IsRelative"] = task_data->IsRelative;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInstrumentMarginRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInstrumentCommissionRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInstrumentCommissionRateField *task_data = (CThostFtdcInstrumentCommissionRateField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OpenRatioByMoney"] = task_data->OpenRatioByMoney;
		data["OpenRatioByVolume"] = task_data->OpenRatioByVolume;
		data["CloseRatioByMoney"] = task_data->CloseRatioByMoney;
		data["CloseRatioByVolume"] = task_data->CloseRatioByVolume;
		data["CloseTodayRatioByMoney"] = task_data->CloseTodayRatioByMoney;
		data["CloseTodayRatioByVolume"] = task_data->CloseTodayRatioByVolume;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["BizType"] = task_data->BizType;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInstrumentCommissionRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryExchange(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExchangeField *task_data = (CThostFtdcExchangeField*)task->task_data;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ExchangeName"] = toUtf(task_data->ExchangeName);
		data["ExchangeProperty"] = task_data->ExchangeProperty;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryExchange(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryProduct(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcProductField *task_data = (CThostFtdcProductField*)task->task_data;
		data["ProductID"] = toUtf(task_data->ProductID);
		data["ProductName"] = toUtf(task_data->ProductName);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ProductClass"] = task_data->ProductClass;
		data["VolumeMultiple"] = task_data->VolumeMultiple;
		data["PriceTick"] = task_data->PriceTick;
		data["MaxMarketOrderVolume"] = task_data->MaxMarketOrderVolume;
		data["MinMarketOrderVolume"] = task_data->MinMarketOrderVolume;
		data["MaxLimitOrderVolume"] = task_data->MaxLimitOrderVolume;
		data["MinLimitOrderVolume"] = task_data->MinLimitOrderVolume;
		data["PositionType"] = task_data->PositionType;
		data["PositionDateType"] = task_data->PositionDateType;
		data["CloseDealType"] = task_data->CloseDealType;
		data["TradeCurrencyID"] = toUtf(task_data->TradeCurrencyID);
		data["MortgageFundUseRange"] = task_data->MortgageFundUseRange;
		data["ExchangeProductID"] = toUtf(task_data->ExchangeProductID);
		data["UnderlyingMultiple"] = task_data->UnderlyingMultiple;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryProduct(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInstrument(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInstrumentField *task_data = (CThostFtdcInstrumentField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InstrumentName"] = toUtf(task_data->InstrumentName);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["ProductID"] = toUtf(task_data->ProductID);
		data["ProductClass"] = task_data->ProductClass;
		data["DeliveryYear"] = task_data->DeliveryYear;
		data["DeliveryMonth"] = task_data->DeliveryMonth;
		data["MaxMarketOrderVolume"] = task_data->MaxMarketOrderVolume;
		data["MinMarketOrderVolume"] = task_data->MinMarketOrderVolume;
		data["MaxLimitOrderVolume"] = task_data->MaxLimitOrderVolume;
		data["MinLimitOrderVolume"] = task_data->MinLimitOrderVolume;
		data["VolumeMultiple"] = task_data->VolumeMultiple;
		data["PriceTick"] = task_data->PriceTick;
		data["CreateDate"] = toUtf(task_data->CreateDate);
		data["OpenDate"] = toUtf(task_data->OpenDate);
		data["ExpireDate"] = toUtf(task_data->ExpireDate);
		data["StartDelivDate"] = toUtf(task_data->StartDelivDate);
		data["EndDelivDate"] = toUtf(task_data->EndDelivDate);
		data["InstLifePhase"] = task_data->InstLifePhase;
		data["IsTrading"] = task_data->IsTrading;
		data["PositionType"] = task_data->PositionType;
		data["PositionDateType"] = task_data->PositionDateType;
		data["LongMarginRatio"] = task_data->LongMarginRatio;
		data["ShortMarginRatio"] = task_data->ShortMarginRatio;
		data["MaxMarginSideAlgorithm"] = task_data->MaxMarginSideAlgorithm;
		data["UnderlyingInstrID"] = toUtf(task_data->UnderlyingInstrID);
		data["StrikePrice"] = task_data->StrikePrice;
		data["OptionsType"] = task_data->OptionsType;
		data["UnderlyingMultiple"] = task_data->UnderlyingMultiple;
		data["CombinationType"] = task_data->CombinationType;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInstrument(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryDepthMarketData(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcDepthMarketDataField *task_data = (CThostFtdcDepthMarketDataField*)task->task_data;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["LastPrice"] = task_data->LastPrice;
		data["PreSettlementPrice"] = task_data->PreSettlementPrice;
		data["PreClosePrice"] = task_data->PreClosePrice;
		data["PreOpenInterest"] = task_data->PreOpenInterest;
		data["OpenPrice"] = task_data->OpenPrice;
		data["HighestPrice"] = task_data->HighestPrice;
		data["LowestPrice"] = task_data->LowestPrice;
		data["Volume"] = task_data->Volume;
		data["Turnover"] = task_data->Turnover;
		data["OpenInterest"] = task_data->OpenInterest;
		data["ClosePrice"] = task_data->ClosePrice;
		data["SettlementPrice"] = task_data->SettlementPrice;
		data["UpperLimitPrice"] = task_data->UpperLimitPrice;
		data["LowerLimitPrice"] = task_data->LowerLimitPrice;
		data["PreDelta"] = task_data->PreDelta;
		data["CurrDelta"] = task_data->CurrDelta;
		data["UpdateTime"] = toUtf(task_data->UpdateTime);
		data["UpdateMillisec"] = task_data->UpdateMillisec;
		data["BidPrice1"] = task_data->BidPrice1;
		data["BidVolume1"] = task_data->BidVolume1;
		data["AskPrice1"] = task_data->AskPrice1;
		data["AskVolume1"] = task_data->AskVolume1;
		data["BidPrice2"] = task_data->BidPrice2;
		data["BidVolume2"] = task_data->BidVolume2;
		data["AskPrice2"] = task_data->AskPrice2;
		data["AskVolume2"] = task_data->AskVolume2;
		data["BidPrice3"] = task_data->BidPrice3;
		data["BidVolume3"] = task_data->BidVolume3;
		data["AskPrice3"] = task_data->AskPrice3;
		data["AskVolume3"] = task_data->AskVolume3;
		data["BidPrice4"] = task_data->BidPrice4;
		data["BidVolume4"] = task_data->BidVolume4;
		data["AskPrice4"] = task_data->AskPrice4;
		data["AskVolume4"] = task_data->AskVolume4;
		data["BidPrice5"] = task_data->BidPrice5;
		data["BidVolume5"] = task_data->BidVolume5;
		data["AskPrice5"] = task_data->AskPrice5;
		data["AskVolume5"] = task_data->AskVolume5;
		data["AveragePrice"] = task_data->AveragePrice;
		data["ActionDay"] = toUtf(task_data->ActionDay);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryDepthMarketData(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQrySettlementInfo(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcSettlementInfoField *task_data = (CThostFtdcSettlementInfoField*)task->task_data;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["Content"] = toUtf(task_data->Content);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQrySettlementInfo(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryTransferBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTransferBankField *task_data = (CThostFtdcTransferBankField*)task->task_data;
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBrchID"] = toUtf(task_data->BankBrchID);
		data["BankName"] = toUtf(task_data->BankName);
		data["IsActive"] = task_data->IsActive;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryTransferBank(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInvestorPositionDetail(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInvestorPositionDetailField *task_data = (CThostFtdcInvestorPositionDetailField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["Direction"] = task_data->Direction;
		data["OpenDate"] = toUtf(task_data->OpenDate);
		data["TradeID"] = toUtf(task_data->TradeID);
		data["Volume"] = task_data->Volume;
		data["OpenPrice"] = task_data->OpenPrice;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["TradeType"] = task_data->TradeType;
		data["CombInstrumentID"] = toUtf(task_data->CombInstrumentID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["CloseProfitByDate"] = task_data->CloseProfitByDate;
		data["CloseProfitByTrade"] = task_data->CloseProfitByTrade;
		data["PositionProfitByDate"] = task_data->PositionProfitByDate;
		data["PositionProfitByTrade"] = task_data->PositionProfitByTrade;
		data["Margin"] = task_data->Margin;
		data["ExchMargin"] = task_data->ExchMargin;
		data["MarginRateByMoney"] = task_data->MarginRateByMoney;
		data["MarginRateByVolume"] = task_data->MarginRateByVolume;
		data["LastSettlementPrice"] = task_data->LastSettlementPrice;
		data["SettlementPrice"] = task_data->SettlementPrice;
		data["CloseVolume"] = task_data->CloseVolume;
		data["CloseAmount"] = task_data->CloseAmount;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInvestorPositionDetail(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryNotice(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcNoticeField *task_data = (CThostFtdcNoticeField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["Content"] = toUtf(task_data->Content);
		data["SequenceLabel"] = toUtf(task_data->SequenceLabel);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryNotice(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQrySettlementInfoConfirm(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcSettlementInfoConfirmField *task_data = (CThostFtdcSettlementInfoConfirmField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ConfirmDate"] = toUtf(task_data->ConfirmDate);
		data["ConfirmTime"] = toUtf(task_data->ConfirmTime);
		data["SettlementID"] = task_data->SettlementID;
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQrySettlementInfoConfirm(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInvestorPositionCombineDetail(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInvestorPositionCombineDetailField *task_data = (CThostFtdcInvestorPositionCombineDetailField*)task->task_data;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["OpenDate"] = toUtf(task_data->OpenDate);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["SettlementID"] = task_data->SettlementID;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ComTradeID"] = toUtf(task_data->ComTradeID);
		data["TradeID"] = toUtf(task_data->TradeID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["Direction"] = task_data->Direction;
		data["TotalAmt"] = task_data->TotalAmt;
		data["Margin"] = task_data->Margin;
		data["ExchMargin"] = task_data->ExchMargin;
		data["MarginRateByMoney"] = task_data->MarginRateByMoney;
		data["MarginRateByVolume"] = task_data->MarginRateByVolume;
		data["LegID"] = task_data->LegID;
		data["LegMultiple"] = task_data->LegMultiple;
		data["CombInstrumentID"] = toUtf(task_data->CombInstrumentID);
		data["TradeGroupID"] = task_data->TradeGroupID;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInvestorPositionCombineDetail(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryCFMMCTradingAccountKey(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcCFMMCTradingAccountKeyField *task_data = (CThostFtdcCFMMCTradingAccountKeyField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["KeyID"] = task_data->KeyID;
		data["CurrentKey"] = toUtf(task_data->CurrentKey);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryCFMMCTradingAccountKey(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryEWarrantOffset(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcEWarrantOffsetField *task_data = (CThostFtdcEWarrantOffsetField*)task->task_data;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["Direction"] = task_data->Direction;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["Volume"] = task_data->Volume;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryEWarrantOffset(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInvestorProductGroupMargin(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInvestorProductGroupMarginField *task_data = (CThostFtdcInvestorProductGroupMarginField*)task->task_data;
		data["ProductGroupID"] = toUtf(task_data->ProductGroupID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["FrozenMargin"] = task_data->FrozenMargin;
		data["LongFrozenMargin"] = task_data->LongFrozenMargin;
		data["ShortFrozenMargin"] = task_data->ShortFrozenMargin;
		data["UseMargin"] = task_data->UseMargin;
		data["LongUseMargin"] = task_data->LongUseMargin;
		data["ShortUseMargin"] = task_data->ShortUseMargin;
		data["ExchMargin"] = task_data->ExchMargin;
		data["LongExchMargin"] = task_data->LongExchMargin;
		data["ShortExchMargin"] = task_data->ShortExchMargin;
		data["CloseProfit"] = task_data->CloseProfit;
		data["FrozenCommission"] = task_data->FrozenCommission;
		data["Commission"] = task_data->Commission;
		data["FrozenCash"] = task_data->FrozenCash;
		data["CashIn"] = task_data->CashIn;
		data["PositionProfit"] = task_data->PositionProfit;
		data["OffsetAmount"] = task_data->OffsetAmount;
		data["LongOffsetAmount"] = task_data->LongOffsetAmount;
		data["ShortOffsetAmount"] = task_data->ShortOffsetAmount;
		data["ExchOffsetAmount"] = task_data->ExchOffsetAmount;
		data["LongExchOffsetAmount"] = task_data->LongExchOffsetAmount;
		data["ShortExchOffsetAmount"] = task_data->ShortExchOffsetAmount;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInvestorProductGroupMargin(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryExchangeMarginRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExchangeMarginRateField *task_data = (CThostFtdcExchangeMarginRateField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["LongMarginRatioByMoney"] = task_data->LongMarginRatioByMoney;
		data["LongMarginRatioByVolume"] = task_data->LongMarginRatioByVolume;
		data["ShortMarginRatioByMoney"] = task_data->ShortMarginRatioByMoney;
		data["ShortMarginRatioByVolume"] = task_data->ShortMarginRatioByVolume;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryExchangeMarginRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryExchangeMarginRateAdjust(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExchangeMarginRateAdjustField *task_data = (CThostFtdcExchangeMarginRateAdjustField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["LongMarginRatioByMoney"] = task_data->LongMarginRatioByMoney;
		data["LongMarginRatioByVolume"] = task_data->LongMarginRatioByVolume;
		data["ShortMarginRatioByMoney"] = task_data->ShortMarginRatioByMoney;
		data["ShortMarginRatioByVolume"] = task_data->ShortMarginRatioByVolume;
		data["ExchLongMarginRatioByMoney"] = task_data->ExchLongMarginRatioByMoney;
		data["ExchLongMarginRatioByVolume"] = task_data->ExchLongMarginRatioByVolume;
		data["ExchShortMarginRatioByMoney"] = task_data->ExchShortMarginRatioByMoney;
		data["ExchShortMarginRatioByVolume"] = task_data->ExchShortMarginRatioByVolume;
		data["NoLongMarginRatioByMoney"] = task_data->NoLongMarginRatioByMoney;
		data["NoLongMarginRatioByVolume"] = task_data->NoLongMarginRatioByVolume;
		data["NoShortMarginRatioByMoney"] = task_data->NoShortMarginRatioByMoney;
		data["NoShortMarginRatioByVolume"] = task_data->NoShortMarginRatioByVolume;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryExchangeMarginRateAdjust(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryExchangeRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExchangeRateField *task_data = (CThostFtdcExchangeRateField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["FromCurrencyID"] = toUtf(task_data->FromCurrencyID);
		data["FromCurrencyUnit"] = task_data->FromCurrencyUnit;
		data["ToCurrencyID"] = toUtf(task_data->ToCurrencyID);
		data["ExchangeRate"] = task_data->ExchangeRate;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryExchangeRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQrySecAgentACIDMap(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcSecAgentACIDMapField *task_data = (CThostFtdcSecAgentACIDMapField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["UserID"] = toUtf(task_data->UserID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["BrokerSecAgentID"] = toUtf(task_data->BrokerSecAgentID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQrySecAgentACIDMap(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryProductExchRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcProductExchRateField *task_data = (CThostFtdcProductExchRateField*)task->task_data;
		data["ProductID"] = toUtf(task_data->ProductID);
		data["QuoteCurrencyID"] = toUtf(task_data->QuoteCurrencyID);
		data["ExchangeRate"] = task_data->ExchangeRate;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryProductExchRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryProductGroup(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcProductGroupField *task_data = (CThostFtdcProductGroupField*)task->task_data;
		data["ProductID"] = toUtf(task_data->ProductID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ProductGroupID"] = toUtf(task_data->ProductGroupID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryProductGroup(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryMMInstrumentCommissionRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcMMInstrumentCommissionRateField *task_data = (CThostFtdcMMInstrumentCommissionRateField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OpenRatioByMoney"] = task_data->OpenRatioByMoney;
		data["OpenRatioByVolume"] = task_data->OpenRatioByVolume;
		data["CloseRatioByMoney"] = task_data->CloseRatioByMoney;
		data["CloseRatioByVolume"] = task_data->CloseRatioByVolume;
		data["CloseTodayRatioByMoney"] = task_data->CloseTodayRatioByMoney;
		data["CloseTodayRatioByVolume"] = task_data->CloseTodayRatioByVolume;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryMMInstrumentCommissionRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryMMOptionInstrCommRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcMMOptionInstrCommRateField *task_data = (CThostFtdcMMOptionInstrCommRateField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OpenRatioByMoney"] = task_data->OpenRatioByMoney;
		data["OpenRatioByVolume"] = task_data->OpenRatioByVolume;
		data["CloseRatioByMoney"] = task_data->CloseRatioByMoney;
		data["CloseRatioByVolume"] = task_data->CloseRatioByVolume;
		data["CloseTodayRatioByMoney"] = task_data->CloseTodayRatioByMoney;
		data["CloseTodayRatioByVolume"] = task_data->CloseTodayRatioByVolume;
		data["StrikeRatioByMoney"] = task_data->StrikeRatioByMoney;
		data["StrikeRatioByVolume"] = task_data->StrikeRatioByVolume;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryMMOptionInstrCommRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInstrumentOrderCommRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInstrumentOrderCommRateField *task_data = (CThostFtdcInstrumentOrderCommRateField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["OrderCommByVolume"] = task_data->OrderCommByVolume;
		data["OrderActionCommByVolume"] = task_data->OrderActionCommByVolume;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInstrumentOrderCommRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQrySecAgentTradingAccount(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradingAccountField *task_data = (CThostFtdcTradingAccountField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["PreMortgage"] = task_data->PreMortgage;
		data["PreCredit"] = task_data->PreCredit;
		data["PreDeposit"] = task_data->PreDeposit;
		data["PreBalance"] = task_data->PreBalance;
		data["PreMargin"] = task_data->PreMargin;
		data["InterestBase"] = task_data->InterestBase;
		data["Interest"] = task_data->Interest;
		data["Deposit"] = task_data->Deposit;
		data["Withdraw"] = task_data->Withdraw;
		data["FrozenMargin"] = task_data->FrozenMargin;
		data["FrozenCash"] = task_data->FrozenCash;
		data["FrozenCommission"] = task_data->FrozenCommission;
		data["CurrMargin"] = task_data->CurrMargin;
		data["CashIn"] = task_data->CashIn;
		data["Commission"] = task_data->Commission;
		data["CloseProfit"] = task_data->CloseProfit;
		data["PositionProfit"] = task_data->PositionProfit;
		data["Balance"] = task_data->Balance;
		data["Available"] = task_data->Available;
		data["WithdrawQuota"] = task_data->WithdrawQuota;
		data["Reserve"] = task_data->Reserve;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["Credit"] = task_data->Credit;
		data["Mortgage"] = task_data->Mortgage;
		data["ExchangeMargin"] = task_data->ExchangeMargin;
		data["DeliveryMargin"] = task_data->DeliveryMargin;
		data["ExchangeDeliveryMargin"] = task_data->ExchangeDeliveryMargin;
		data["ReserveBalance"] = task_data->ReserveBalance;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["PreFundMortgageIn"] = task_data->PreFundMortgageIn;
		data["PreFundMortgageOut"] = task_data->PreFundMortgageOut;
		data["FundMortgageIn"] = task_data->FundMortgageIn;
		data["FundMortgageOut"] = task_data->FundMortgageOut;
		data["FundMortgageAvailable"] = task_data->FundMortgageAvailable;
		data["MortgageableFund"] = task_data->MortgageableFund;
		data["SpecProductMargin"] = task_data->SpecProductMargin;
		data["SpecProductFrozenMargin"] = task_data->SpecProductFrozenMargin;
		data["SpecProductCommission"] = task_data->SpecProductCommission;
		data["SpecProductFrozenCommission"] = task_data->SpecProductFrozenCommission;
		data["SpecProductPositionProfit"] = task_data->SpecProductPositionProfit;
		data["SpecProductCloseProfit"] = task_data->SpecProductCloseProfit;
		data["SpecProductPositionProfitByAlg"] = task_data->SpecProductPositionProfitByAlg;
		data["SpecProductExchangeMargin"] = task_data->SpecProductExchangeMargin;
		data["BizType"] = task_data->BizType;
		data["FrozenSwap"] = task_data->FrozenSwap;
		data["RemainSwap"] = task_data->RemainSwap;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQrySecAgentTradingAccount(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQrySecAgentCheckMode(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcSecAgentCheckModeField *task_data = (CThostFtdcSecAgentCheckModeField*)task->task_data;
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["BrokerSecAgentID"] = toUtf(task_data->BrokerSecAgentID);
		data["CheckSelfAccount"] = task_data->CheckSelfAccount;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQrySecAgentCheckMode(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQrySecAgentTradeInfo(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcSecAgentTradeInfoField *task_data = (CThostFtdcSecAgentTradeInfoField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerSecAgentID"] = toUtf(task_data->BrokerSecAgentID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQrySecAgentTradeInfo(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryOptionInstrTradeCost(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOptionInstrTradeCostField *task_data = (CThostFtdcOptionInstrTradeCostField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["FixedMargin"] = task_data->FixedMargin;
		data["MiniMargin"] = task_data->MiniMargin;
		data["Royalty"] = task_data->Royalty;
		data["ExchFixedMargin"] = task_data->ExchFixedMargin;
		data["ExchMiniMargin"] = task_data->ExchMiniMargin;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryOptionInstrTradeCost(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryOptionInstrCommRate(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOptionInstrCommRateField *task_data = (CThostFtdcOptionInstrCommRateField*)task->task_data;
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OpenRatioByMoney"] = task_data->OpenRatioByMoney;
		data["OpenRatioByVolume"] = task_data->OpenRatioByVolume;
		data["CloseRatioByMoney"] = task_data->CloseRatioByMoney;
		data["CloseRatioByVolume"] = task_data->CloseRatioByVolume;
		data["CloseTodayRatioByMoney"] = task_data->CloseTodayRatioByMoney;
		data["CloseTodayRatioByVolume"] = task_data->CloseTodayRatioByVolume;
		data["StrikeRatioByMoney"] = task_data->StrikeRatioByMoney;
		data["StrikeRatioByVolume"] = task_data->StrikeRatioByVolume;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryOptionInstrCommRate(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryExecOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExecOrderField *task_data = (CThostFtdcExecOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ExecOrderRef"] = toUtf(task_data->ExecOrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ActionType"] = task_data->ActionType;
		data["PosiDirection"] = task_data->PosiDirection;
		data["ReservePositionFlag"] = task_data->ReservePositionFlag;
		data["CloseFlag"] = task_data->CloseFlag;
		data["ExecOrderLocalID"] = toUtf(task_data->ExecOrderLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["ExecOrderSysID"] = toUtf(task_data->ExecOrderSysID);
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ExecResult"] = task_data->ExecResult;
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerExecOrderSeq"] = task_data->BrokerExecOrderSeq;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryExecOrder(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryForQuote(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcForQuoteField *task_data = (CThostFtdcForQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ForQuoteRef"] = toUtf(task_data->ForQuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["ForQuoteLocalID"] = toUtf(task_data->ForQuoteLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["ForQuoteStatus"] = task_data->ForQuoteStatus;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerForQutoSeq"] = task_data->BrokerForQutoSeq;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryForQuote(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryQuote(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcQuoteField *task_data = (CThostFtdcQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["QuoteRef"] = toUtf(task_data->QuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["AskPrice"] = task_data->AskPrice;
		data["BidPrice"] = task_data->BidPrice;
		data["AskVolume"] = task_data->AskVolume;
		data["BidVolume"] = task_data->BidVolume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["AskOffsetFlag"] = task_data->AskOffsetFlag;
		data["BidOffsetFlag"] = task_data->BidOffsetFlag;
		data["AskHedgeFlag"] = task_data->AskHedgeFlag;
		data["BidHedgeFlag"] = task_data->BidHedgeFlag;
		data["QuoteLocalID"] = toUtf(task_data->QuoteLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["NotifySequence"] = task_data->NotifySequence;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["QuoteSysID"] = toUtf(task_data->QuoteSysID);
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["QuoteStatus"] = task_data->QuoteStatus;
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["AskOrderSysID"] = toUtf(task_data->AskOrderSysID);
		data["BidOrderSysID"] = toUtf(task_data->BidOrderSysID);
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerQuoteSeq"] = task_data->BrokerQuoteSeq;
		data["AskOrderRef"] = toUtf(task_data->AskOrderRef);
		data["BidOrderRef"] = toUtf(task_data->BidOrderRef);
		data["ForQuoteSysID"] = toUtf(task_data->ForQuoteSysID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryQuote(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryOptionSelfClose(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOptionSelfCloseField *task_data = (CThostFtdcOptionSelfCloseField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OptionSelfCloseRef"] = toUtf(task_data->OptionSelfCloseRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["OptSelfCloseFlag"] = task_data->OptSelfCloseFlag;
		data["OptionSelfCloseLocalID"] = toUtf(task_data->OptionSelfCloseLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["OptionSelfCloseSysID"] = toUtf(task_data->OptionSelfCloseSysID);
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ExecResult"] = task_data->ExecResult;
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerOptionSelfCloseSeq"] = task_data->BrokerOptionSelfCloseSeq;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryOptionSelfClose(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryInvestUnit(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInvestUnitField *task_data = (CThostFtdcInvestUnitField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["InvestorUnitName"] = toUtf(task_data->InvestorUnitName);
		data["InvestorGroupID"] = toUtf(task_data->InvestorGroupID);
		data["CommModelID"] = toUtf(task_data->CommModelID);
		data["MarginModelID"] = toUtf(task_data->MarginModelID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryInvestUnit(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryCombInstrumentGuard(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcCombInstrumentGuardField *task_data = (CThostFtdcCombInstrumentGuardField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["GuarantRatio"] = task_data->GuarantRatio;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryCombInstrumentGuard(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryCombAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcCombActionField *task_data = (CThostFtdcCombActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["CombActionRef"] = toUtf(task_data->CombActionRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Direction"] = task_data->Direction;
		data["Volume"] = task_data->Volume;
		data["CombDirection"] = task_data->CombDirection;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["ActionStatus"] = task_data->ActionStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		data["ComTradeID"] = toUtf(task_data->ComTradeID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryCombAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryTransferSerial(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTransferSerialField *task_data = (CThostFtdcTransferSerialField*)task->task_data;
		data["PlateSerial"] = task_data->PlateSerial;
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["SessionID"] = task_data->SessionID;
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BankAccType"] = task_data->BankAccType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["FutureAccType"] = task_data->FutureAccType;
		data["AccountID"] = toUtf(task_data->AccountID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["FutureSerial"] = task_data->FutureSerial;
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["AvailabilityFlag"] = task_data->AvailabilityFlag;
		data["OperatorCode"] = toUtf(task_data->OperatorCode);
		data["BankNewAccount"] = toUtf(task_data->BankNewAccount);
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryTransferSerial(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryAccountregister(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcAccountregisterField *task_data = (CThostFtdcAccountregisterField*)task->task_data;
		data["TradeDay"] = toUtf(task_data->TradeDay);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["OpenOrDestroy"] = task_data->OpenOrDestroy;
		data["RegDate"] = toUtf(task_data->RegDate);
		data["OutDate"] = toUtf(task_data->OutDate);
		data["TID"] = task_data->TID;
		data["CustType"] = task_data->CustType;
		data["BankAccType"] = task_data->BankAccType;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryAccountregister(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspError(Task *task)
{
	gil_scoped_acquire acquire;
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspError(error, task->task_id, task->task_last);
};

void TdApiApp::processRtnOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOrderField *task_data = (CThostFtdcOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["OrderLocalID"] = toUtf(task_data->OrderLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["OrderSource"] = task_data->OrderSource;
		data["OrderStatus"] = task_data->OrderStatus;
		data["OrderType"] = task_data->OrderType;
		data["VolumeTraded"] = task_data->VolumeTraded;
		data["VolumeTotal"] = task_data->VolumeTotal;
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["ActiveTime"] = toUtf(task_data->ActiveTime);
		data["SuspendTime"] = toUtf(task_data->SuspendTime);
		data["UpdateTime"] = toUtf(task_data->UpdateTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ActiveTraderID"] = toUtf(task_data->ActiveTraderID);
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["UserForceClose"] = task_data->UserForceClose;
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerOrderSeq"] = task_data->BrokerOrderSeq;
		data["RelativeOrderSysID"] = toUtf(task_data->RelativeOrderSysID);
		data["ZCETotalTradedVolume"] = task_data->ZCETotalTradedVolume;
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	this->onRtnOrder(data);
};

void TdApiApp::processRtnTrade(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradeField *task_data = (CThostFtdcTradeField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["TradeID"] = toUtf(task_data->TradeID);
		data["Direction"] = task_data->Direction;
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["TradingRole"] = task_data->TradingRole;
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["Price"] = task_data->Price;
		data["Volume"] = task_data->Volume;
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["TradeType"] = task_data->TradeType;
		data["PriceSource"] = task_data->PriceSource;
		data["TraderID"] = toUtf(task_data->TraderID);
		data["OrderLocalID"] = toUtf(task_data->OrderLocalID);
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["SequenceNo"] = task_data->SequenceNo;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["BrokerOrderSeq"] = task_data->BrokerOrderSeq;
		data["TradeSource"] = task_data->TradeSource;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	this->onRtnTrade(data);
};

void TdApiApp::processErrRtnOrderInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputOrderField *task_data = (CThostFtdcInputOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["UserForceClose"] = task_data->UserForceClose;
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnOrderInsert(data, error);
};

void TdApiApp::processErrRtnOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOrderActionField *task_data = (CThostFtdcOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OrderActionRef"] = task_data->OrderActionRef;
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeChange"] = task_data->VolumeChange;
		data["ActionDate"] = toUtf(task_data->ActionDate);
		data["ActionTime"] = toUtf(task_data->ActionTime);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderLocalID"] = toUtf(task_data->OrderLocalID);
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OrderActionStatus"] = task_data->OrderActionStatus;
		data["UserID"] = toUtf(task_data->UserID);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnOrderAction(data, error);
};

void TdApiApp::processRtnInstrumentStatus(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInstrumentStatusField *task_data = (CThostFtdcInstrumentStatusField*)task->task_data;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["SettlementGroupID"] = toUtf(task_data->SettlementGroupID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["InstrumentStatus"] = task_data->InstrumentStatus;
		data["TradingSegmentSN"] = task_data->TradingSegmentSN;
		data["EnterTime"] = toUtf(task_data->EnterTime);
		data["EnterReason"] = task_data->EnterReason;
		delete task_data;
	}
	this->onRtnInstrumentStatus(data);
};

void TdApiApp::processRtnBulletin(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcBulletinField *task_data = (CThostFtdcBulletinField*)task->task_data;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["BulletinID"] = task_data->BulletinID;
		data["SequenceNo"] = task_data->SequenceNo;
		data["NewsType"] = toUtf(task_data->NewsType);
		data["NewsUrgency"] = task_data->NewsUrgency;
		data["SendTime"] = toUtf(task_data->SendTime);
		data["Abstract"] = toUtf(task_data->Abstract);
		data["ComeFrom"] = toUtf(task_data->ComeFrom);
		data["Content"] = toUtf(task_data->Content);
		data["URLLink"] = toUtf(task_data->URLLink);
		data["MarketID"] = toUtf(task_data->MarketID);
		delete task_data;
	}
	this->onRtnBulletin(data);
};

void TdApiApp::processRtnTradingNotice(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradingNoticeInfoField *task_data = (CThostFtdcTradingNoticeInfoField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["SendTime"] = toUtf(task_data->SendTime);
		data["FieldContent"] = toUtf(task_data->FieldContent);
		data["SequenceSeries"] = task_data->SequenceSeries;
		data["SequenceNo"] = task_data->SequenceNo;
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	this->onRtnTradingNotice(data);
};

void TdApiApp::processRtnErrorConditionalOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcErrorConditionalOrderField *task_data = (CThostFtdcErrorConditionalOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["OrderLocalID"] = toUtf(task_data->OrderLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["OrderSource"] = task_data->OrderSource;
		data["OrderStatus"] = task_data->OrderStatus;
		data["OrderType"] = task_data->OrderType;
		data["VolumeTraded"] = task_data->VolumeTraded;
		data["VolumeTotal"] = task_data->VolumeTotal;
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["ActiveTime"] = toUtf(task_data->ActiveTime);
		data["SuspendTime"] = toUtf(task_data->SuspendTime);
		data["UpdateTime"] = toUtf(task_data->UpdateTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ActiveTraderID"] = toUtf(task_data->ActiveTraderID);
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["UserForceClose"] = task_data->UserForceClose;
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerOrderSeq"] = task_data->BrokerOrderSeq;
		data["RelativeOrderSysID"] = toUtf(task_data->RelativeOrderSysID);
		data["ZCETotalTradedVolume"] = task_data->ZCETotalTradedVolume;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	this->onRtnErrorConditionalOrder(data);
};

void TdApiApp::processRtnExecOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExecOrderField *task_data = (CThostFtdcExecOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ExecOrderRef"] = toUtf(task_data->ExecOrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ActionType"] = task_data->ActionType;
		data["PosiDirection"] = task_data->PosiDirection;
		data["ReservePositionFlag"] = task_data->ReservePositionFlag;
		data["CloseFlag"] = task_data->CloseFlag;
		data["ExecOrderLocalID"] = toUtf(task_data->ExecOrderLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["ExecOrderSysID"] = toUtf(task_data->ExecOrderSysID);
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ExecResult"] = task_data->ExecResult;
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerExecOrderSeq"] = task_data->BrokerExecOrderSeq;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	this->onRtnExecOrder(data);
};

void TdApiApp::processErrRtnExecOrderInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputExecOrderField *task_data = (CThostFtdcInputExecOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ExecOrderRef"] = toUtf(task_data->ExecOrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OffsetFlag"] = task_data->OffsetFlag;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ActionType"] = task_data->ActionType;
		data["PosiDirection"] = task_data->PosiDirection;
		data["ReservePositionFlag"] = task_data->ReservePositionFlag;
		data["CloseFlag"] = task_data->CloseFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnExecOrderInsert(data, error);
};

void TdApiApp::processErrRtnExecOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcExecOrderActionField *task_data = (CThostFtdcExecOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["ExecOrderActionRef"] = task_data->ExecOrderActionRef;
		data["ExecOrderRef"] = toUtf(task_data->ExecOrderRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ExecOrderSysID"] = toUtf(task_data->ExecOrderSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["ActionDate"] = toUtf(task_data->ActionDate);
		data["ActionTime"] = toUtf(task_data->ActionTime);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["ExecOrderLocalID"] = toUtf(task_data->ExecOrderLocalID);
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OrderActionStatus"] = task_data->OrderActionStatus;
		data["UserID"] = toUtf(task_data->UserID);
		data["ActionType"] = task_data->ActionType;
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnExecOrderAction(data, error);
};

void TdApiApp::processErrRtnForQuoteInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputForQuoteField *task_data = (CThostFtdcInputForQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ForQuoteRef"] = toUtf(task_data->ForQuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnForQuoteInsert(data, error);
};

void TdApiApp::processRtnQuote(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcQuoteField *task_data = (CThostFtdcQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["QuoteRef"] = toUtf(task_data->QuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["AskPrice"] = task_data->AskPrice;
		data["BidPrice"] = task_data->BidPrice;
		data["AskVolume"] = task_data->AskVolume;
		data["BidVolume"] = task_data->BidVolume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["AskOffsetFlag"] = task_data->AskOffsetFlag;
		data["BidOffsetFlag"] = task_data->BidOffsetFlag;
		data["AskHedgeFlag"] = task_data->AskHedgeFlag;
		data["BidHedgeFlag"] = task_data->BidHedgeFlag;
		data["QuoteLocalID"] = toUtf(task_data->QuoteLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["NotifySequence"] = task_data->NotifySequence;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["QuoteSysID"] = toUtf(task_data->QuoteSysID);
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["QuoteStatus"] = task_data->QuoteStatus;
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["AskOrderSysID"] = toUtf(task_data->AskOrderSysID);
		data["BidOrderSysID"] = toUtf(task_data->BidOrderSysID);
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerQuoteSeq"] = task_data->BrokerQuoteSeq;
		data["AskOrderRef"] = toUtf(task_data->AskOrderRef);
		data["BidOrderRef"] = toUtf(task_data->BidOrderRef);
		data["ForQuoteSysID"] = toUtf(task_data->ForQuoteSysID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	this->onRtnQuote(data);
};

void TdApiApp::processErrRtnQuoteInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputQuoteField *task_data = (CThostFtdcInputQuoteField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["QuoteRef"] = toUtf(task_data->QuoteRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["AskPrice"] = task_data->AskPrice;
		data["BidPrice"] = task_data->BidPrice;
		data["AskVolume"] = task_data->AskVolume;
		data["BidVolume"] = task_data->BidVolume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["AskOffsetFlag"] = task_data->AskOffsetFlag;
		data["BidOffsetFlag"] = task_data->BidOffsetFlag;
		data["AskHedgeFlag"] = task_data->AskHedgeFlag;
		data["BidHedgeFlag"] = task_data->BidHedgeFlag;
		data["AskOrderRef"] = toUtf(task_data->AskOrderRef);
		data["BidOrderRef"] = toUtf(task_data->BidOrderRef);
		data["ForQuoteSysID"] = toUtf(task_data->ForQuoteSysID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnQuoteInsert(data, error);
};

void TdApiApp::processErrRtnQuoteAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcQuoteActionField *task_data = (CThostFtdcQuoteActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["QuoteActionRef"] = task_data->QuoteActionRef;
		data["QuoteRef"] = toUtf(task_data->QuoteRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["QuoteSysID"] = toUtf(task_data->QuoteSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["ActionDate"] = toUtf(task_data->ActionDate);
		data["ActionTime"] = toUtf(task_data->ActionTime);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["QuoteLocalID"] = toUtf(task_data->QuoteLocalID);
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OrderActionStatus"] = task_data->OrderActionStatus;
		data["UserID"] = toUtf(task_data->UserID);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnQuoteAction(data, error);
};

void TdApiApp::processRtnForQuoteRsp(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcForQuoteRspField *task_data = (CThostFtdcForQuoteRspField*)task->task_data;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ForQuoteSysID"] = toUtf(task_data->ForQuoteSysID);
		data["ForQuoteTime"] = toUtf(task_data->ForQuoteTime);
		data["ActionDay"] = toUtf(task_data->ActionDay);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		delete task_data;
	}
	this->onRtnForQuoteRsp(data);
};

void TdApiApp::processRtnCFMMCTradingAccountToken(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcCFMMCTradingAccountTokenField *task_data = (CThostFtdcCFMMCTradingAccountTokenField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["KeyID"] = task_data->KeyID;
		data["Token"] = toUtf(task_data->Token);
		delete task_data;
	}
	this->onRtnCFMMCTradingAccountToken(data);
};

void TdApiApp::processErrRtnBatchOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcBatchOrderActionField *task_data = (CThostFtdcBatchOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OrderActionRef"] = task_data->OrderActionRef;
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ActionDate"] = toUtf(task_data->ActionDate);
		data["ActionTime"] = toUtf(task_data->ActionTime);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OrderActionStatus"] = task_data->OrderActionStatus;
		data["UserID"] = toUtf(task_data->UserID);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnBatchOrderAction(data, error);
};

void TdApiApp::processRtnOptionSelfClose(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOptionSelfCloseField *task_data = (CThostFtdcOptionSelfCloseField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OptionSelfCloseRef"] = toUtf(task_data->OptionSelfCloseRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["OptSelfCloseFlag"] = task_data->OptSelfCloseFlag;
		data["OptionSelfCloseLocalID"] = toUtf(task_data->OptionSelfCloseLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OrderSubmitStatus"] = task_data->OrderSubmitStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["OptionSelfCloseSysID"] = toUtf(task_data->OptionSelfCloseSysID);
		data["InsertDate"] = toUtf(task_data->InsertDate);
		data["InsertTime"] = toUtf(task_data->InsertTime);
		data["CancelTime"] = toUtf(task_data->CancelTime);
		data["ExecResult"] = task_data->ExecResult;
		data["ClearingPartID"] = toUtf(task_data->ClearingPartID);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["ActiveUserID"] = toUtf(task_data->ActiveUserID);
		data["BrokerOptionSelfCloseSeq"] = task_data->BrokerOptionSelfCloseSeq;
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	this->onRtnOptionSelfClose(data);
};

void TdApiApp::processErrRtnOptionSelfCloseInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputOptionSelfCloseField *task_data = (CThostFtdcInputOptionSelfCloseField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OptionSelfCloseRef"] = toUtf(task_data->OptionSelfCloseRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Volume"] = task_data->Volume;
		data["RequestID"] = task_data->RequestID;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["OptSelfCloseFlag"] = task_data->OptSelfCloseFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnOptionSelfCloseInsert(data, error);
};

void TdApiApp::processErrRtnOptionSelfCloseAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOptionSelfCloseActionField *task_data = (CThostFtdcOptionSelfCloseActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OptionSelfCloseActionRef"] = task_data->OptionSelfCloseActionRef;
		data["OptionSelfCloseRef"] = toUtf(task_data->OptionSelfCloseRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["OptionSelfCloseSysID"] = toUtf(task_data->OptionSelfCloseSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["ActionDate"] = toUtf(task_data->ActionDate);
		data["ActionTime"] = toUtf(task_data->ActionTime);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["OptionSelfCloseLocalID"] = toUtf(task_data->OptionSelfCloseLocalID);
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["OrderActionStatus"] = task_data->OrderActionStatus;
		data["UserID"] = toUtf(task_data->UserID);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnOptionSelfCloseAction(data, error);
};

void TdApiApp::processRtnCombAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcCombActionField *task_data = (CThostFtdcCombActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["CombActionRef"] = toUtf(task_data->CombActionRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Direction"] = task_data->Direction;
		data["Volume"] = task_data->Volume;
		data["CombDirection"] = task_data->CombDirection;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ActionLocalID"] = toUtf(task_data->ActionLocalID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParticipantID"] = toUtf(task_data->ParticipantID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["ExchangeInstID"] = toUtf(task_data->ExchangeInstID);
		data["TraderID"] = toUtf(task_data->TraderID);
		data["InstallID"] = task_data->InstallID;
		data["ActionStatus"] = task_data->ActionStatus;
		data["NotifySequence"] = task_data->NotifySequence;
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["SettlementID"] = task_data->SettlementID;
		data["SequenceNo"] = task_data->SequenceNo;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["UserProductInfo"] = toUtf(task_data->UserProductInfo);
		data["StatusMsg"] = toUtf(task_data->StatusMsg);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		data["ComTradeID"] = toUtf(task_data->ComTradeID);
		data["BranchID"] = toUtf(task_data->BranchID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	this->onRtnCombAction(data);
};

void TdApiApp::processErrRtnCombActionInsert(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcInputCombActionField *task_data = (CThostFtdcInputCombActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["CombActionRef"] = toUtf(task_data->CombActionRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["Direction"] = task_data->Direction;
		data["Volume"] = task_data->Volume;
		data["CombDirection"] = task_data->CombDirection;
		data["HedgeFlag"] = task_data->HedgeFlag;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnCombActionInsert(data, error);
};

void TdApiApp::processRspQryContractBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcContractBankField *task_data = (CThostFtdcContractBankField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBrchID"] = toUtf(task_data->BankBrchID);
		data["BankName"] = toUtf(task_data->BankName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryContractBank(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryParkedOrder(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcParkedOrderField *task_data = (CThostFtdcParkedOrderField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["UserID"] = toUtf(task_data->UserID);
		data["OrderPriceType"] = task_data->OrderPriceType;
		data["Direction"] = task_data->Direction;
		data["CombOffsetFlag"] = toUtf(task_data->CombOffsetFlag);
		data["CombHedgeFlag"] = toUtf(task_data->CombHedgeFlag);
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeTotalOriginal"] = task_data->VolumeTotalOriginal;
		data["TimeCondition"] = task_data->TimeCondition;
		data["GTDDate"] = toUtf(task_data->GTDDate);
		data["VolumeCondition"] = task_data->VolumeCondition;
		data["MinVolume"] = task_data->MinVolume;
		data["ContingentCondition"] = task_data->ContingentCondition;
		data["StopPrice"] = task_data->StopPrice;
		data["ForceCloseReason"] = task_data->ForceCloseReason;
		data["IsAutoSuspend"] = task_data->IsAutoSuspend;
		data["BusinessUnit"] = toUtf(task_data->BusinessUnit);
		data["RequestID"] = task_data->RequestID;
		data["UserForceClose"] = task_data->UserForceClose;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["ParkedOrderID"] = toUtf(task_data->ParkedOrderID);
		data["UserType"] = task_data->UserType;
		data["Status"] = task_data->Status;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["IsSwapOrder"] = task_data->IsSwapOrder;
		data["AccountID"] = toUtf(task_data->AccountID);
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["ClientID"] = toUtf(task_data->ClientID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryParkedOrder(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryParkedOrderAction(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcParkedOrderActionField *task_data = (CThostFtdcParkedOrderActionField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["OrderActionRef"] = task_data->OrderActionRef;
		data["OrderRef"] = toUtf(task_data->OrderRef);
		data["RequestID"] = task_data->RequestID;
		data["FrontID"] = task_data->FrontID;
		data["SessionID"] = task_data->SessionID;
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["OrderSysID"] = toUtf(task_data->OrderSysID);
		data["ActionFlag"] = task_data->ActionFlag;
		data["LimitPrice"] = task_data->LimitPrice;
		data["VolumeChange"] = task_data->VolumeChange;
		data["UserID"] = toUtf(task_data->UserID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["ParkedOrderActionID"] = toUtf(task_data->ParkedOrderActionID);
		data["UserType"] = task_data->UserType;
		data["Status"] = task_data->Status;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		data["IPAddress"] = toUtf(task_data->IPAddress);
		data["MacAddress"] = toUtf(task_data->MacAddress);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryParkedOrderAction(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryTradingNotice(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcTradingNoticeField *task_data = (CThostFtdcTradingNoticeField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorRange"] = task_data->InvestorRange;
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["SequenceSeries"] = task_data->SequenceSeries;
		data["UserID"] = toUtf(task_data->UserID);
		data["SendTime"] = toUtf(task_data->SendTime);
		data["SequenceNo"] = task_data->SequenceNo;
		data["FieldContent"] = toUtf(task_data->FieldContent);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryTradingNotice(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryBrokerTradingParams(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcBrokerTradingParamsField *task_data = (CThostFtdcBrokerTradingParamsField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["MarginPriceType"] = task_data->MarginPriceType;
		data["Algorithm"] = task_data->Algorithm;
		data["AvailIncludeCloseProfit"] = task_data->AvailIncludeCloseProfit;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["OptionRoyaltyPriceType"] = task_data->OptionRoyaltyPriceType;
		data["AccountID"] = toUtf(task_data->AccountID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryBrokerTradingParams(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQryBrokerTradingAlgos(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcBrokerTradingAlgosField *task_data = (CThostFtdcBrokerTradingAlgosField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["ExchangeID"] = toUtf(task_data->ExchangeID);
		data["InstrumentID"] = toUtf(task_data->InstrumentID);
		data["HandlePositionAlgoID"] = task_data->HandlePositionAlgoID;
		data["FindMarginRateAlgoID"] = task_data->FindMarginRateAlgoID;
		data["HandleTradingAccountAlgoID"] = task_data->HandleTradingAccountAlgoID;
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQryBrokerTradingAlgos(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQueryCFMMCTradingAccountToken(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcQueryCFMMCTradingAccountTokenField *task_data = (CThostFtdcQueryCFMMCTradingAccountTokenField*)task->task_data;
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["InvestorID"] = toUtf(task_data->InvestorID);
		data["InvestUnitID"] = toUtf(task_data->InvestUnitID);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQueryCFMMCTradingAccountToken(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRtnFromBankToFutureByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspTransferField *task_data = (CThostFtdcRspTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnFromBankToFutureByBank(data);
};

void TdApiApp::processRtnFromFutureToBankByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspTransferField *task_data = (CThostFtdcRspTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnFromFutureToBankByBank(data);
};

void TdApiApp::processRtnRepealFromBankToFutureByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspRepealField *task_data = (CThostFtdcRspRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnRepealFromBankToFutureByBank(data);
};

void TdApiApp::processRtnRepealFromFutureToBankByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspRepealField *task_data = (CThostFtdcRspRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnRepealFromFutureToBankByBank(data);
};

void TdApiApp::processRtnFromBankToFutureByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspTransferField *task_data = (CThostFtdcRspTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnFromBankToFutureByFuture(data);
};

void TdApiApp::processRtnFromFutureToBankByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspTransferField *task_data = (CThostFtdcRspTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnFromFutureToBankByFuture(data);
};

void TdApiApp::processRtnRepealFromBankToFutureByFutureManual(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspRepealField *task_data = (CThostFtdcRspRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnRepealFromBankToFutureByFutureManual(data);
};

void TdApiApp::processRtnRepealFromFutureToBankByFutureManual(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspRepealField *task_data = (CThostFtdcRspRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnRepealFromFutureToBankByFutureManual(data);
};

void TdApiApp::processRtnQueryBankBalanceByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcNotifyQueryAccountField *task_data = (CThostFtdcNotifyQueryAccountField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["FutureSerial"] = task_data->FutureSerial;
		data["InstallID"] = task_data->InstallID;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["BankUseAmount"] = task_data->BankUseAmount;
		data["BankFetchAmount"] = task_data->BankFetchAmount;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnQueryBankBalanceByFuture(data);
};

void TdApiApp::processErrRtnBankToFutureByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqTransferField *task_data = (CThostFtdcReqTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnBankToFutureByFuture(data, error);
};

void TdApiApp::processErrRtnFutureToBankByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqTransferField *task_data = (CThostFtdcReqTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnFutureToBankByFuture(data, error);
};

void TdApiApp::processErrRtnRepealBankToFutureByFutureManual(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqRepealField *task_data = (CThostFtdcReqRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnRepealBankToFutureByFutureManual(data, error);
};

void TdApiApp::processErrRtnRepealFutureToBankByFutureManual(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqRepealField *task_data = (CThostFtdcReqRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnRepealFutureToBankByFutureManual(data, error);
};

void TdApiApp::processErrRtnQueryBankBalanceByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqQueryAccountField *task_data = (CThostFtdcReqQueryAccountField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["FutureSerial"] = task_data->FutureSerial;
		data["InstallID"] = task_data->InstallID;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onErrRtnQueryBankBalanceByFuture(data, error);
};

void TdApiApp::processRtnRepealFromBankToFutureByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspRepealField *task_data = (CThostFtdcRspRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnRepealFromBankToFutureByFuture(data);
};

void TdApiApp::processRtnRepealFromFutureToBankByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcRspRepealField *task_data = (CThostFtdcRspRepealField*)task->task_data;
		data["RepealTimeInterval"] = task_data->RepealTimeInterval;
		data["RepealedTimes"] = task_data->RepealedTimes;
		data["BankRepealFlag"] = task_data->BankRepealFlag;
		data["BrokerRepealFlag"] = task_data->BrokerRepealFlag;
		data["PlateRepealSerial"] = task_data->PlateRepealSerial;
		data["BankRepealSerial"] = toUtf(task_data->BankRepealSerial);
		data["FutureRepealSerial"] = task_data->FutureRepealSerial;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnRepealFromFutureToBankByFuture(data);
};

void TdApiApp::processRspFromBankToFutureByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqTransferField *task_data = (CThostFtdcReqTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspFromBankToFutureByFuture(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspFromFutureToBankByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqTransferField *task_data = (CThostFtdcReqTransferField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["FutureSerial"] = task_data->FutureSerial;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["TradeAmount"] = task_data->TradeAmount;
		data["FutureFetchAmount"] = task_data->FutureFetchAmount;
		data["FeePayFlag"] = task_data->FeePayFlag;
		data["CustFee"] = task_data->CustFee;
		data["BrokerFee"] = task_data->BrokerFee;
		data["Message"] = toUtf(task_data->Message);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["TransferStatus"] = task_data->TransferStatus;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspFromFutureToBankByFuture(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRspQueryBankAccountMoneyByFuture(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcReqQueryAccountField *task_data = (CThostFtdcReqQueryAccountField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["CustType"] = task_data->CustType;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["FutureSerial"] = task_data->FutureSerial;
		data["InstallID"] = task_data->InstallID;
		data["UserID"] = toUtf(task_data->UserID);
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["RequestID"] = task_data->RequestID;
		data["TID"] = task_data->TID;
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	dict error;
	if (task->task_error)
	{
		CThostFtdcRspInfoField *task_error = (CThostFtdcRspInfoField*)task->task_error;
		error["ErrorID"] = task_error->ErrorID;
		error["ErrorMsg"] = toUtf(task_error->ErrorMsg);
		delete task_error;
	}
	this->onRspQueryBankAccountMoneyByFuture(data, error, task->task_id, task->task_last);
};

void TdApiApp::processRtnOpenAccountByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcOpenAccountField *task_data = (CThostFtdcOpenAccountField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["Gender"] = task_data->Gender;
		data["CountryCode"] = toUtf(task_data->CountryCode);
		data["CustType"] = task_data->CustType;
		data["Address"] = toUtf(task_data->Address);
		data["ZipCode"] = toUtf(task_data->ZipCode);
		data["Telephone"] = toUtf(task_data->Telephone);
		data["MobilePhone"] = toUtf(task_data->MobilePhone);
		data["Fax"] = toUtf(task_data->Fax);
		data["EMail"] = toUtf(task_data->EMail);
		data["MoneyAccountStatus"] = task_data->MoneyAccountStatus;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["CashExchangeCode"] = task_data->CashExchangeCode;
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["TID"] = task_data->TID;
		data["UserID"] = toUtf(task_data->UserID);
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnOpenAccountByBank(data);
};

void TdApiApp::processRtnCancelAccountByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcCancelAccountField *task_data = (CThostFtdcCancelAccountField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["Gender"] = task_data->Gender;
		data["CountryCode"] = toUtf(task_data->CountryCode);
		data["CustType"] = task_data->CustType;
		data["Address"] = toUtf(task_data->Address);
		data["ZipCode"] = toUtf(task_data->ZipCode);
		data["Telephone"] = toUtf(task_data->Telephone);
		data["MobilePhone"] = toUtf(task_data->MobilePhone);
		data["Fax"] = toUtf(task_data->Fax);
		data["EMail"] = toUtf(task_data->EMail);
		data["MoneyAccountStatus"] = task_data->MoneyAccountStatus;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["InstallID"] = task_data->InstallID;
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["CashExchangeCode"] = task_data->CashExchangeCode;
		data["Digest"] = toUtf(task_data->Digest);
		data["BankAccType"] = task_data->BankAccType;
		data["DeviceID"] = toUtf(task_data->DeviceID);
		data["BankSecuAccType"] = task_data->BankSecuAccType;
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankSecuAcc"] = toUtf(task_data->BankSecuAcc);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["OperNo"] = toUtf(task_data->OperNo);
		data["TID"] = task_data->TID;
		data["UserID"] = toUtf(task_data->UserID);
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnCancelAccountByBank(data);
};

void TdApiApp::processRtnChangeAccountByBank(Task *task)
{
	gil_scoped_acquire acquire;
	dict data;
	if (task->task_data)
	{
		CThostFtdcChangeAccountField *task_data = (CThostFtdcChangeAccountField*)task->task_data;
		data["TradeCode"] = toUtf(task_data->TradeCode);
		data["BankID"] = toUtf(task_data->BankID);
		data["BankBranchID"] = toUtf(task_data->BankBranchID);
		data["BrokerID"] = toUtf(task_data->BrokerID);
		data["BrokerBranchID"] = toUtf(task_data->BrokerBranchID);
		data["TradeDate"] = toUtf(task_data->TradeDate);
		data["TradeTime"] = toUtf(task_data->TradeTime);
		data["BankSerial"] = toUtf(task_data->BankSerial);
		data["TradingDay"] = toUtf(task_data->TradingDay);
		data["PlateSerial"] = task_data->PlateSerial;
		data["LastFragment"] = task_data->LastFragment;
		data["SessionID"] = task_data->SessionID;
		data["CustomerName"] = toUtf(task_data->CustomerName);
		data["IdCardType"] = task_data->IdCardType;
		data["IdentifiedCardNo"] = toUtf(task_data->IdentifiedCardNo);
		data["Gender"] = task_data->Gender;
		data["CountryCode"] = toUtf(task_data->CountryCode);
		data["CustType"] = task_data->CustType;
		data["Address"] = toUtf(task_data->Address);
		data["ZipCode"] = toUtf(task_data->ZipCode);
		data["Telephone"] = toUtf(task_data->Telephone);
		data["MobilePhone"] = toUtf(task_data->MobilePhone);
		data["Fax"] = toUtf(task_data->Fax);
		data["EMail"] = toUtf(task_data->EMail);
		data["MoneyAccountStatus"] = task_data->MoneyAccountStatus;
		data["BankAccount"] = toUtf(task_data->BankAccount);
		data["BankPassWord"] = toUtf(task_data->BankPassWord);
		data["NewBankAccount"] = toUtf(task_data->NewBankAccount);
		data["NewBankPassWord"] = toUtf(task_data->NewBankPassWord);
		data["AccountID"] = toUtf(task_data->AccountID);
		data["Password"] = toUtf(task_data->Password);
		data["BankAccType"] = task_data->BankAccType;
		data["InstallID"] = task_data->InstallID;
		data["VerifyCertNoFlag"] = task_data->VerifyCertNoFlag;
		data["CurrencyID"] = toUtf(task_data->CurrencyID);
		data["BrokerIDByBank"] = toUtf(task_data->BrokerIDByBank);
		data["BankPwdFlag"] = task_data->BankPwdFlag;
		data["SecuPwdFlag"] = task_data->SecuPwdFlag;
		data["TID"] = task_data->TID;
		data["Digest"] = toUtf(task_data->Digest);
		data["ErrorID"] = task_data->ErrorID;
		data["ErrorMsg"] = toUtf(task_data->ErrorMsg);
		data["LongCustomerName"] = toUtf(task_data->LongCustomerName);
		delete task_data;
	}
	this->onRtnChangeAccountByBank(data);
};


///-------------------------------------------------------------------------------------
///主动函数
///-------------------------------------------------------------------------------------

void TdApiApp::createFtdcTraderApi(string pszFlowPath)
{
    this->api = CThostFtdcTraderApi::CreateFtdcTraderApi(pszFlowPath.c_str());
    this->api->RegisterSpi(this);
};

void TdApiApp::release()
{
    this->api->Release();
};

void TdApiApp::init()
{
    this->active = true;
    this->task_thread = thread(&TdApiApp::processTask, this);

    this->api->Init();
};

int TdApiApp::join()
{
    int i = this->api->Join();
    return i;
};

int TdApiApp::exit()
{
    this->active = false;
    this->task_queue.terminate();
    this->task_thread.join();

    this->api->RegisterSpi(NULL);
    this->api->Release();
    this->api = NULL;
    return 1;
};

string TdApiApp::getTradingDay()
{
    string day = this->api->GetTradingDay();
    return day;
};

void TdApiApp::registerFront(string pszFrontAddress)
{
    this->api->RegisterFront((char*)pszFrontAddress.c_str());
};

void TdApiApp::subscribePrivateTopic(int nType)
{
    this->api->SubscribePrivateTopic((THOST_TE_RESUME_TYPE) nType);
};

void TdApiApp::subscribePublicTopic(int nType)
{
    this->api->SubscribePublicTopic((THOST_TE_RESUME_TYPE)nType);
};

int TdApiApp::reqAuthenticate(const dict &req, int reqid)
{
	CThostFtdcReqAuthenticateField myreq = CThostFtdcReqAuthenticateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "UserProductInfo", myreq.UserProductInfo);
	getString(req, "AuthCode", myreq.AuthCode);
	getString(req, "AppID", myreq.AppID);
	int i = this->api->ReqAuthenticate(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserLogin(const dict &req, int reqid)
{
	CThostFtdcReqUserLoginField myreq = CThostFtdcReqUserLoginField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "Password", myreq.Password);
	getString(req, "UserProductInfo", myreq.UserProductInfo);
	getString(req, "InterfaceProductInfo", myreq.InterfaceProductInfo);
	getString(req, "ProtocolInfo", myreq.ProtocolInfo);
	getString(req, "MacAddress", myreq.MacAddress);
	getString(req, "OneTimePassword", myreq.OneTimePassword);
	getString(req, "ClientIPAddress", myreq.ClientIPAddress);
	getString(req, "LoginRemark", myreq.LoginRemark);
	getInt(req, "ClientIPPort", &myreq.ClientIPPort);
	int i = this->api->ReqUserLogin(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserLogout(const dict &req, int reqid)
{
	CThostFtdcUserLogoutField myreq = CThostFtdcUserLogoutField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	int i = this->api->ReqUserLogout(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserPasswordUpdate(const dict &req, int reqid)
{
	CThostFtdcUserPasswordUpdateField myreq = CThostFtdcUserPasswordUpdateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "OldPassword", myreq.OldPassword);
	getString(req, "NewPassword", myreq.NewPassword);
	int i = this->api->ReqUserPasswordUpdate(&myreq, reqid);
	return i;
};

int TdApiApp::reqTradingAccountPasswordUpdate(const dict &req, int reqid)
{
	CThostFtdcTradingAccountPasswordUpdateField myreq = CThostFtdcTradingAccountPasswordUpdateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "OldPassword", myreq.OldPassword);
	getString(req, "NewPassword", myreq.NewPassword);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqTradingAccountPasswordUpdate(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserAuthMethod(const dict &req, int reqid)
{
	CThostFtdcReqUserAuthMethodField myreq = CThostFtdcReqUserAuthMethodField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	int i = this->api->ReqUserAuthMethod(&myreq, reqid);
	return i;
};

int TdApiApp::reqGenUserCaptcha(const dict &req, int reqid)
{
	CThostFtdcReqGenUserCaptchaField myreq = CThostFtdcReqGenUserCaptchaField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	int i = this->api->ReqGenUserCaptcha(&myreq, reqid);
	return i;
};

int TdApiApp::reqGenUserText(const dict &req, int reqid)
{
	CThostFtdcReqGenUserTextField myreq = CThostFtdcReqGenUserTextField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	int i = this->api->ReqGenUserText(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserLoginWithCaptcha(const dict &req, int reqid)
{
	CThostFtdcReqUserLoginWithCaptchaField myreq = CThostFtdcReqUserLoginWithCaptchaField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "Password", myreq.Password);
	getString(req, "UserProductInfo", myreq.UserProductInfo);
	getString(req, "InterfaceProductInfo", myreq.InterfaceProductInfo);
	getString(req, "ProtocolInfo", myreq.ProtocolInfo);
	getString(req, "MacAddress", myreq.MacAddress);
	getString(req, "ClientIPAddress", myreq.ClientIPAddress);
	getString(req, "LoginRemark", myreq.LoginRemark);
	getString(req, "Captcha", myreq.Captcha);
	getInt(req, "ClientIPPort", &myreq.ClientIPPort);
	int i = this->api->ReqUserLoginWithCaptcha(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserLoginWithText(const dict &req, int reqid)
{
	CThostFtdcReqUserLoginWithTextField myreq = CThostFtdcReqUserLoginWithTextField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "Password", myreq.Password);
	getString(req, "UserProductInfo", myreq.UserProductInfo);
	getString(req, "InterfaceProductInfo", myreq.InterfaceProductInfo);
	getString(req, "ProtocolInfo", myreq.ProtocolInfo);
	getString(req, "MacAddress", myreq.MacAddress);
	getString(req, "ClientIPAddress", myreq.ClientIPAddress);
	getString(req, "LoginRemark", myreq.LoginRemark);
	getString(req, "Text", myreq.Text);
	getInt(req, "ClientIPPort", &myreq.ClientIPPort);
	int i = this->api->ReqUserLoginWithText(&myreq, reqid);
	return i;
};

int TdApiApp::reqUserLoginWithOTP(const dict &req, int reqid)
{
	CThostFtdcReqUserLoginWithOTPField myreq = CThostFtdcReqUserLoginWithOTPField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "Password", myreq.Password);
	getString(req, "UserProductInfo", myreq.UserProductInfo);
	getString(req, "InterfaceProductInfo", myreq.InterfaceProductInfo);
	getString(req, "ProtocolInfo", myreq.ProtocolInfo);
	getString(req, "MacAddress", myreq.MacAddress);
	getString(req, "ClientIPAddress", myreq.ClientIPAddress);
	getString(req, "LoginRemark", myreq.LoginRemark);
	getString(req, "OTPPassword", myreq.OTPPassword);
	getInt(req, "ClientIPPort", &myreq.ClientIPPort);
	int i = this->api->ReqUserLoginWithOTP(&myreq, reqid);
	return i;
};

int TdApiApp::reqOrderInsert(const dict &req, int reqid)
{
	CThostFtdcInputOrderField myreq = CThostFtdcInputOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "OrderRef", myreq.OrderRef);
	getString(req, "UserID", myreq.UserID);
	getChar(req, "OrderPriceType", &myreq.OrderPriceType);
	getChar(req, "Direction", &myreq.Direction);
	getString(req, "CombOffsetFlag", myreq.CombOffsetFlag);
	getString(req, "CombHedgeFlag", myreq.CombHedgeFlag);
	getDouble(req, "LimitPrice", &myreq.LimitPrice);
	getInt(req, "VolumeTotalOriginal", &myreq.VolumeTotalOriginal);
	getChar(req, "TimeCondition", &myreq.TimeCondition);
	getString(req, "GTDDate", myreq.GTDDate);
	getChar(req, "VolumeCondition", &myreq.VolumeCondition);
	getInt(req, "MinVolume", &myreq.MinVolume);
	getChar(req, "ContingentCondition", &myreq.ContingentCondition);
	getDouble(req, "StopPrice", &myreq.StopPrice);
	getChar(req, "ForceCloseReason", &myreq.ForceCloseReason);
	getInt(req, "IsAutoSuspend", &myreq.IsAutoSuspend);
	getString(req, "BusinessUnit", myreq.BusinessUnit);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "UserForceClose", &myreq.UserForceClose);
	getInt(req, "IsSwapOrder", &myreq.IsSwapOrder);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getString(req, "ClientID", myreq.ClientID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqOrderInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqParkedOrderInsert(const dict &req, int reqid)
{
	CThostFtdcParkedOrderField myreq = CThostFtdcParkedOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "OrderRef", myreq.OrderRef);
	getString(req, "UserID", myreq.UserID);
	getChar(req, "OrderPriceType", &myreq.OrderPriceType);
	getChar(req, "Direction", &myreq.Direction);
	getString(req, "CombOffsetFlag", myreq.CombOffsetFlag);
	getString(req, "CombHedgeFlag", myreq.CombHedgeFlag);
	getDouble(req, "LimitPrice", &myreq.LimitPrice);
	getInt(req, "VolumeTotalOriginal", &myreq.VolumeTotalOriginal);
	getChar(req, "TimeCondition", &myreq.TimeCondition);
	getString(req, "GTDDate", myreq.GTDDate);
	getChar(req, "VolumeCondition", &myreq.VolumeCondition);
	getInt(req, "MinVolume", &myreq.MinVolume);
	getChar(req, "ContingentCondition", &myreq.ContingentCondition);
	getDouble(req, "StopPrice", &myreq.StopPrice);
	getChar(req, "ForceCloseReason", &myreq.ForceCloseReason);
	getInt(req, "IsAutoSuspend", &myreq.IsAutoSuspend);
	getString(req, "BusinessUnit", myreq.BusinessUnit);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "UserForceClose", &myreq.UserForceClose);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "ParkedOrderID", myreq.ParkedOrderID);
	getChar(req, "UserType", &myreq.UserType);
	getChar(req, "Status", &myreq.Status);
	getInt(req, "ErrorID", &myreq.ErrorID);
	getString(req, "ErrorMsg", myreq.ErrorMsg);
	getInt(req, "IsSwapOrder", &myreq.IsSwapOrder);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getString(req, "ClientID", myreq.ClientID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqParkedOrderInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqParkedOrderAction(const dict &req, int reqid)
{
	CThostFtdcParkedOrderActionField myreq = CThostFtdcParkedOrderActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getInt(req, "OrderActionRef", &myreq.OrderActionRef);
	getString(req, "OrderRef", myreq.OrderRef);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "FrontID", &myreq.FrontID);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "OrderSysID", myreq.OrderSysID);
	getChar(req, "ActionFlag", &myreq.ActionFlag);
	getDouble(req, "LimitPrice", &myreq.LimitPrice);
	getInt(req, "VolumeChange", &myreq.VolumeChange);
	getString(req, "UserID", myreq.UserID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ParkedOrderActionID", myreq.ParkedOrderActionID);
	getChar(req, "UserType", &myreq.UserType);
	getChar(req, "Status", &myreq.Status);
	getInt(req, "ErrorID", &myreq.ErrorID);
	getString(req, "ErrorMsg", myreq.ErrorMsg);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqParkedOrderAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqOrderAction(const dict &req, int reqid)
{
	CThostFtdcInputOrderActionField myreq = CThostFtdcInputOrderActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getInt(req, "OrderActionRef", &myreq.OrderActionRef);
	getString(req, "OrderRef", myreq.OrderRef);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "FrontID", &myreq.FrontID);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "OrderSysID", myreq.OrderSysID);
	getChar(req, "ActionFlag", &myreq.ActionFlag);
	getDouble(req, "LimitPrice", &myreq.LimitPrice);
	getInt(req, "VolumeChange", &myreq.VolumeChange);
	getString(req, "UserID", myreq.UserID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqOrderAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqQueryMaxOrderVolume(const dict &req, int reqid)
{
	CThostFtdcQueryMaxOrderVolumeField myreq = CThostFtdcQueryMaxOrderVolumeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getChar(req, "Direction", &myreq.Direction);
	getChar(req, "OffsetFlag", &myreq.OffsetFlag);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getInt(req, "MaxVolume", &myreq.MaxVolume);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQueryMaxOrderVolume(&myreq, reqid);
	return i;
};

int TdApiApp::reqSettlementInfoConfirm(const dict &req, int reqid)
{
	CThostFtdcSettlementInfoConfirmField myreq = CThostFtdcSettlementInfoConfirmField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "ConfirmDate", myreq.ConfirmDate);
	getString(req, "ConfirmTime", myreq.ConfirmTime);
	getInt(req, "SettlementID", &myreq.SettlementID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqSettlementInfoConfirm(&myreq, reqid);
	return i;
};

int TdApiApp::reqRemoveParkedOrder(const dict &req, int reqid)
{
	CThostFtdcRemoveParkedOrderField myreq = CThostFtdcRemoveParkedOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "ParkedOrderID", myreq.ParkedOrderID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqRemoveParkedOrder(&myreq, reqid);
	return i;
};

int TdApiApp::reqRemoveParkedOrderAction(const dict &req, int reqid)
{
	CThostFtdcRemoveParkedOrderActionField myreq = CThostFtdcRemoveParkedOrderActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "ParkedOrderActionID", myreq.ParkedOrderActionID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqRemoveParkedOrderAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqExecOrderInsert(const dict &req, int reqid)
{
	CThostFtdcInputExecOrderField myreq = CThostFtdcInputExecOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExecOrderRef", myreq.ExecOrderRef);
	getString(req, "UserID", myreq.UserID);
	getInt(req, "Volume", &myreq.Volume);
	getInt(req, "RequestID", &myreq.RequestID);
	getString(req, "BusinessUnit", myreq.BusinessUnit);
	getChar(req, "OffsetFlag", &myreq.OffsetFlag);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getChar(req, "ActionType", &myreq.ActionType);
	getChar(req, "PosiDirection", &myreq.PosiDirection);
	getChar(req, "ReservePositionFlag", &myreq.ReservePositionFlag);
	getChar(req, "CloseFlag", &myreq.CloseFlag);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getString(req, "ClientID", myreq.ClientID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqExecOrderInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqExecOrderAction(const dict &req, int reqid)
{
	CThostFtdcInputExecOrderActionField myreq = CThostFtdcInputExecOrderActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getInt(req, "ExecOrderActionRef", &myreq.ExecOrderActionRef);
	getString(req, "ExecOrderRef", myreq.ExecOrderRef);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "FrontID", &myreq.FrontID);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "ExecOrderSysID", myreq.ExecOrderSysID);
	getChar(req, "ActionFlag", &myreq.ActionFlag);
	getString(req, "UserID", myreq.UserID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqExecOrderAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqForQuoteInsert(const dict &req, int reqid)
{
	CThostFtdcInputForQuoteField myreq = CThostFtdcInputForQuoteField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ForQuoteRef", myreq.ForQuoteRef);
	getString(req, "UserID", myreq.UserID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqForQuoteInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqQuoteInsert(const dict &req, int reqid)
{
	CThostFtdcInputQuoteField myreq = CThostFtdcInputQuoteField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "QuoteRef", myreq.QuoteRef);
	getString(req, "UserID", myreq.UserID);
	getDouble(req, "AskPrice", &myreq.AskPrice);
	getDouble(req, "BidPrice", &myreq.BidPrice);
	getInt(req, "AskVolume", &myreq.AskVolume);
	getInt(req, "BidVolume", &myreq.BidVolume);
	getInt(req, "RequestID", &myreq.RequestID);
	getString(req, "BusinessUnit", myreq.BusinessUnit);
	getChar(req, "AskOffsetFlag", &myreq.AskOffsetFlag);
	getChar(req, "BidOffsetFlag", &myreq.BidOffsetFlag);
	getChar(req, "AskHedgeFlag", &myreq.AskHedgeFlag);
	getChar(req, "BidHedgeFlag", &myreq.BidHedgeFlag);
	getString(req, "AskOrderRef", myreq.AskOrderRef);
	getString(req, "BidOrderRef", myreq.BidOrderRef);
	getString(req, "ForQuoteSysID", myreq.ForQuoteSysID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "ClientID", myreq.ClientID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqQuoteInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqQuoteAction(const dict &req, int reqid)
{
	CThostFtdcInputQuoteActionField myreq = CThostFtdcInputQuoteActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getInt(req, "QuoteActionRef", &myreq.QuoteActionRef);
	getString(req, "QuoteRef", myreq.QuoteRef);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "FrontID", &myreq.FrontID);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "QuoteSysID", myreq.QuoteSysID);
	getChar(req, "ActionFlag", &myreq.ActionFlag);
	getString(req, "UserID", myreq.UserID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "ClientID", myreq.ClientID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqQuoteAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqBatchOrderAction(const dict &req, int reqid)
{
	CThostFtdcInputBatchOrderActionField myreq = CThostFtdcInputBatchOrderActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getInt(req, "OrderActionRef", &myreq.OrderActionRef);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "FrontID", &myreq.FrontID);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqBatchOrderAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqOptionSelfCloseInsert(const dict &req, int reqid)
{
	CThostFtdcInputOptionSelfCloseField myreq = CThostFtdcInputOptionSelfCloseField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "OptionSelfCloseRef", myreq.OptionSelfCloseRef);
	getString(req, "UserID", myreq.UserID);
	getInt(req, "Volume", &myreq.Volume);
	getInt(req, "RequestID", &myreq.RequestID);
	getString(req, "BusinessUnit", myreq.BusinessUnit);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getChar(req, "OptSelfCloseFlag", &myreq.OptSelfCloseFlag);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getString(req, "ClientID", myreq.ClientID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqOptionSelfCloseInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqOptionSelfCloseAction(const dict &req, int reqid)
{
	CThostFtdcInputOptionSelfCloseActionField myreq = CThostFtdcInputOptionSelfCloseActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getInt(req, "OptionSelfCloseActionRef", &myreq.OptionSelfCloseActionRef);
	getString(req, "OptionSelfCloseRef", myreq.OptionSelfCloseRef);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "FrontID", &myreq.FrontID);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "OptionSelfCloseSysID", myreq.OptionSelfCloseSysID);
	getChar(req, "ActionFlag", &myreq.ActionFlag);
	getString(req, "UserID", myreq.UserID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	int i = this->api->ReqOptionSelfCloseAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqCombActionInsert(const dict &req, int reqid)
{
	CThostFtdcInputCombActionField myreq = CThostFtdcInputCombActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "CombActionRef", myreq.CombActionRef);
	getString(req, "UserID", myreq.UserID);
	getChar(req, "Direction", &myreq.Direction);
	getInt(req, "Volume", &myreq.Volume);
	getChar(req, "CombDirection", &myreq.CombDirection);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "IPAddress", myreq.IPAddress);
	getString(req, "MacAddress", myreq.MacAddress);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqCombActionInsert(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryOrder(const dict &req, int reqid)
{
	CThostFtdcQryOrderField myreq = CThostFtdcQryOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "OrderSysID", myreq.OrderSysID);
	getString(req, "InsertTimeStart", myreq.InsertTimeStart);
	getString(req, "InsertTimeEnd", myreq.InsertTimeEnd);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryOrder(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryTrade(const dict &req, int reqid)
{
	CThostFtdcQryTradeField myreq = CThostFtdcQryTradeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "TradeID", myreq.TradeID);
	getString(req, "TradeTimeStart", myreq.TradeTimeStart);
	getString(req, "TradeTimeEnd", myreq.TradeTimeEnd);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryTrade(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInvestorPosition(const dict &req, int reqid)
{
	CThostFtdcQryInvestorPositionField myreq = CThostFtdcQryInvestorPositionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInvestorPosition(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryTradingAccount(const dict &req, int reqid)
{
	CThostFtdcQryTradingAccountField myreq = CThostFtdcQryTradingAccountField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getChar(req, "BizType", &myreq.BizType);
	getString(req, "AccountID", myreq.AccountID);
	int i = this->api->ReqQryTradingAccount(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInvestor(const dict &req, int reqid)
{
	CThostFtdcQryInvestorField myreq = CThostFtdcQryInvestorField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	int i = this->api->ReqQryInvestor(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryTradingCode(const dict &req, int reqid)
{
	CThostFtdcQryTradingCodeField myreq = CThostFtdcQryTradingCodeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "ClientID", myreq.ClientID);
	getChar(req, "ClientIDType", &myreq.ClientIDType);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryTradingCode(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInstrumentMarginRate(const dict &req, int reqid)
{
	CThostFtdcQryInstrumentMarginRateField myreq = CThostFtdcQryInstrumentMarginRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInstrumentMarginRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInstrumentCommissionRate(const dict &req, int reqid)
{
	CThostFtdcQryInstrumentCommissionRateField myreq = CThostFtdcQryInstrumentCommissionRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInstrumentCommissionRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryExchange(const dict &req, int reqid)
{
	CThostFtdcQryExchangeField myreq = CThostFtdcQryExchangeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryExchange(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryProduct(const dict &req, int reqid)
{
	CThostFtdcQryProductField myreq = CThostFtdcQryProductField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "ProductID", myreq.ProductID);
	getChar(req, "ProductClass", &myreq.ProductClass);
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryProduct(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInstrument(const dict &req, int reqid)
{
	CThostFtdcQryInstrumentField myreq = CThostFtdcQryInstrumentField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "ExchangeInstID", myreq.ExchangeInstID);
	getString(req, "ProductID", myreq.ProductID);
	int i = this->api->ReqQryInstrument(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryDepthMarketData(const dict &req, int reqid)
{
	CThostFtdcQryDepthMarketDataField myreq = CThostFtdcQryDepthMarketDataField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryDepthMarketData(&myreq, reqid);
	return i;
};

int TdApiApp::reqQrySettlementInfo(const dict &req, int reqid)
{
	CThostFtdcQrySettlementInfoField myreq = CThostFtdcQrySettlementInfoField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "TradingDay", myreq.TradingDay);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqQrySettlementInfo(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryTransferBank(const dict &req, int reqid)
{
	CThostFtdcQryTransferBankField myreq = CThostFtdcQryTransferBankField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BankID", myreq.BankID);
	getString(req, "BankBrchID", myreq.BankBrchID);
	int i = this->api->ReqQryTransferBank(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInvestorPositionDetail(const dict &req, int reqid)
{
	CThostFtdcQryInvestorPositionDetailField myreq = CThostFtdcQryInvestorPositionDetailField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInvestorPositionDetail(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryNotice(const dict &req, int reqid)
{
	CThostFtdcQryNoticeField myreq = CThostFtdcQryNoticeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	int i = this->api->ReqQryNotice(&myreq, reqid);
	return i;
};

int TdApiApp::reqQrySettlementInfoConfirm(const dict &req, int reqid)
{
	CThostFtdcQrySettlementInfoConfirmField myreq = CThostFtdcQrySettlementInfoConfirmField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqQrySettlementInfoConfirm(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInvestorPositionCombineDetail(const dict &req, int reqid)
{
	CThostFtdcQryInvestorPositionCombineDetailField myreq = CThostFtdcQryInvestorPositionCombineDetailField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "CombInstrumentID", myreq.CombInstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInvestorPositionCombineDetail(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryCFMMCTradingAccountKey(const dict &req, int reqid)
{
	CThostFtdcQryCFMMCTradingAccountKeyField myreq = CThostFtdcQryCFMMCTradingAccountKeyField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	int i = this->api->ReqQryCFMMCTradingAccountKey(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryEWarrantOffset(const dict &req, int reqid)
{
	CThostFtdcQryEWarrantOffsetField myreq = CThostFtdcQryEWarrantOffsetField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryEWarrantOffset(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInvestorProductGroupMargin(const dict &req, int reqid)
{
	CThostFtdcQryInvestorProductGroupMarginField myreq = CThostFtdcQryInvestorProductGroupMarginField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "ProductGroupID", myreq.ProductGroupID);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInvestorProductGroupMargin(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryExchangeMarginRate(const dict &req, int reqid)
{
	CThostFtdcQryExchangeMarginRateField myreq = CThostFtdcQryExchangeMarginRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryExchangeMarginRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryExchangeMarginRateAdjust(const dict &req, int reqid)
{
	CThostFtdcQryExchangeMarginRateAdjustField myreq = CThostFtdcQryExchangeMarginRateAdjustField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	int i = this->api->ReqQryExchangeMarginRateAdjust(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryExchangeRate(const dict &req, int reqid)
{
	CThostFtdcQryExchangeRateField myreq = CThostFtdcQryExchangeRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "FromCurrencyID", myreq.FromCurrencyID);
	getString(req, "ToCurrencyID", myreq.ToCurrencyID);
	int i = this->api->ReqQryExchangeRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQrySecAgentACIDMap(const dict &req, int reqid)
{
	CThostFtdcQrySecAgentACIDMapField myreq = CThostFtdcQrySecAgentACIDMapField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "UserID", myreq.UserID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqQrySecAgentACIDMap(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryProductExchRate(const dict &req, int reqid)
{
	CThostFtdcQryProductExchRateField myreq = CThostFtdcQryProductExchRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "ProductID", myreq.ProductID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryProductExchRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryProductGroup(const dict &req, int reqid)
{
	CThostFtdcQryProductGroupField myreq = CThostFtdcQryProductGroupField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "ProductID", myreq.ProductID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryProductGroup(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryMMInstrumentCommissionRate(const dict &req, int reqid)
{
	CThostFtdcQryMMInstrumentCommissionRateField myreq = CThostFtdcQryMMInstrumentCommissionRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	int i = this->api->ReqQryMMInstrumentCommissionRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryMMOptionInstrCommRate(const dict &req, int reqid)
{
	CThostFtdcQryMMOptionInstrCommRateField myreq = CThostFtdcQryMMOptionInstrCommRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	int i = this->api->ReqQryMMOptionInstrCommRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInstrumentOrderCommRate(const dict &req, int reqid)
{
	CThostFtdcQryInstrumentOrderCommRateField myreq = CThostFtdcQryInstrumentOrderCommRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	int i = this->api->ReqQryInstrumentOrderCommRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQrySecAgentTradingAccount(const dict &req, int reqid)
{
	CThostFtdcQryTradingAccountField myreq = CThostFtdcQryTradingAccountField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getChar(req, "BizType", &myreq.BizType);
	getString(req, "AccountID", myreq.AccountID);
	int i = this->api->ReqQrySecAgentTradingAccount(&myreq, reqid);
	return i;
};

int TdApiApp::reqQrySecAgentCheckMode(const dict &req, int reqid)
{
	CThostFtdcQrySecAgentCheckModeField myreq = CThostFtdcQrySecAgentCheckModeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	int i = this->api->ReqQrySecAgentCheckMode(&myreq, reqid);
	return i;
};

int TdApiApp::reqQrySecAgentTradeInfo(const dict &req, int reqid)
{
	CThostFtdcQrySecAgentTradeInfoField myreq = CThostFtdcQrySecAgentTradeInfoField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "BrokerSecAgentID", myreq.BrokerSecAgentID);
	int i = this->api->ReqQrySecAgentTradeInfo(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryOptionInstrTradeCost(const dict &req, int reqid)
{
	CThostFtdcQryOptionInstrTradeCostField myreq = CThostFtdcQryOptionInstrTradeCostField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getChar(req, "HedgeFlag", &myreq.HedgeFlag);
	getDouble(req, "InputPrice", &myreq.InputPrice);
	getDouble(req, "UnderlyingPrice", &myreq.UnderlyingPrice);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryOptionInstrTradeCost(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryOptionInstrCommRate(const dict &req, int reqid)
{
	CThostFtdcQryOptionInstrCommRateField myreq = CThostFtdcQryOptionInstrCommRateField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryOptionInstrCommRate(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryExecOrder(const dict &req, int reqid)
{
	CThostFtdcQryExecOrderField myreq = CThostFtdcQryExecOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "ExecOrderSysID", myreq.ExecOrderSysID);
	getString(req, "InsertTimeStart", myreq.InsertTimeStart);
	getString(req, "InsertTimeEnd", myreq.InsertTimeEnd);
	int i = this->api->ReqQryExecOrder(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryForQuote(const dict &req, int reqid)
{
	CThostFtdcQryForQuoteField myreq = CThostFtdcQryForQuoteField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InsertTimeStart", myreq.InsertTimeStart);
	getString(req, "InsertTimeEnd", myreq.InsertTimeEnd);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryForQuote(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryQuote(const dict &req, int reqid)
{
	CThostFtdcQryQuoteField myreq = CThostFtdcQryQuoteField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "QuoteSysID", myreq.QuoteSysID);
	getString(req, "InsertTimeStart", myreq.InsertTimeStart);
	getString(req, "InsertTimeEnd", myreq.InsertTimeEnd);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryQuote(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryOptionSelfClose(const dict &req, int reqid)
{
	CThostFtdcQryOptionSelfCloseField myreq = CThostFtdcQryOptionSelfCloseField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "OptionSelfCloseSysID", myreq.OptionSelfCloseSysID);
	getString(req, "InsertTimeStart", myreq.InsertTimeStart);
	getString(req, "InsertTimeEnd", myreq.InsertTimeEnd);
	int i = this->api->ReqQryOptionSelfClose(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryInvestUnit(const dict &req, int reqid)
{
	CThostFtdcQryInvestUnitField myreq = CThostFtdcQryInvestUnitField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryInvestUnit(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryCombInstrumentGuard(const dict &req, int reqid)
{
	CThostFtdcQryCombInstrumentGuardField myreq = CThostFtdcQryCombInstrumentGuardField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	int i = this->api->ReqQryCombInstrumentGuard(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryCombAction(const dict &req, int reqid)
{
	CThostFtdcQryCombActionField myreq = CThostFtdcQryCombActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryCombAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryTransferSerial(const dict &req, int reqid)
{
	CThostFtdcQryTransferSerialField myreq = CThostFtdcQryTransferSerialField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "BankID", myreq.BankID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqQryTransferSerial(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryAccountregister(const dict &req, int reqid)
{
	CThostFtdcQryAccountregisterField myreq = CThostFtdcQryAccountregisterField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "BankID", myreq.BankID);
	getString(req, "BankBranchID", myreq.BankBranchID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	int i = this->api->ReqQryAccountregister(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryContractBank(const dict &req, int reqid)
{
	CThostFtdcQryContractBankField myreq = CThostFtdcQryContractBankField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "BankID", myreq.BankID);
	getString(req, "BankBrchID", myreq.BankBrchID);
	int i = this->api->ReqQryContractBank(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryParkedOrder(const dict &req, int reqid)
{
	CThostFtdcQryParkedOrderField myreq = CThostFtdcQryParkedOrderField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryParkedOrder(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryParkedOrderAction(const dict &req, int reqid)
{
	CThostFtdcQryParkedOrderActionField myreq = CThostFtdcQryParkedOrderActionField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryParkedOrderAction(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryTradingNotice(const dict &req, int reqid)
{
	CThostFtdcQryTradingNoticeField myreq = CThostFtdcQryTradingNoticeField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQryTradingNotice(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryBrokerTradingParams(const dict &req, int reqid)
{
	CThostFtdcQryBrokerTradingParamsField myreq = CThostFtdcQryBrokerTradingParamsField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getString(req, "AccountID", myreq.AccountID);
	int i = this->api->ReqQryBrokerTradingParams(&myreq, reqid);
	return i;
};

int TdApiApp::reqQryBrokerTradingAlgos(const dict &req, int reqid)
{
	CThostFtdcQryBrokerTradingAlgosField myreq = CThostFtdcQryBrokerTradingAlgosField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "ExchangeID", myreq.ExchangeID);
	getString(req, "InstrumentID", myreq.InstrumentID);
	int i = this->api->ReqQryBrokerTradingAlgos(&myreq, reqid);
	return i;
};

int TdApiApp::reqQueryCFMMCTradingAccountToken(const dict &req, int reqid)
{
	CThostFtdcQueryCFMMCTradingAccountTokenField myreq = CThostFtdcQueryCFMMCTradingAccountTokenField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "InvestorID", myreq.InvestorID);
	getString(req, "InvestUnitID", myreq.InvestUnitID);
	int i = this->api->ReqQueryCFMMCTradingAccountToken(&myreq, reqid);
	return i;
};

int TdApiApp::reqFromBankToFutureByFuture(const dict &req, int reqid)
{
	CThostFtdcReqTransferField myreq = CThostFtdcReqTransferField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradeCode", myreq.TradeCode);
	getString(req, "BankID", myreq.BankID);
	getString(req, "BankBranchID", myreq.BankBranchID);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "BrokerBranchID", myreq.BrokerBranchID);
	getString(req, "TradeDate", myreq.TradeDate);
	getString(req, "TradeTime", myreq.TradeTime);
	getString(req, "BankSerial", myreq.BankSerial);
	getString(req, "TradingDay", myreq.TradingDay);
	getInt(req, "PlateSerial", &myreq.PlateSerial);
	getChar(req, "LastFragment", &myreq.LastFragment);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "CustomerName", myreq.CustomerName);
	getChar(req, "IdCardType", &myreq.IdCardType);
	getString(req, "IdentifiedCardNo", myreq.IdentifiedCardNo);
	getChar(req, "CustType", &myreq.CustType);
	getString(req, "BankAccount", myreq.BankAccount);
	getString(req, "BankPassWord", myreq.BankPassWord);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "Password", myreq.Password);
	getInt(req, "InstallID", &myreq.InstallID);
	getInt(req, "FutureSerial", &myreq.FutureSerial);
	getString(req, "UserID", myreq.UserID);
	getChar(req, "VerifyCertNoFlag", &myreq.VerifyCertNoFlag);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getDouble(req, "TradeAmount", &myreq.TradeAmount);
	getDouble(req, "FutureFetchAmount", &myreq.FutureFetchAmount);
	getChar(req, "FeePayFlag", &myreq.FeePayFlag);
	getDouble(req, "CustFee", &myreq.CustFee);
	getDouble(req, "BrokerFee", &myreq.BrokerFee);
	getString(req, "Message", myreq.Message);
	getString(req, "Digest", myreq.Digest);
	getChar(req, "BankAccType", &myreq.BankAccType);
	getString(req, "DeviceID", myreq.DeviceID);
	getChar(req, "BankSecuAccType", &myreq.BankSecuAccType);
	getString(req, "BrokerIDByBank", myreq.BrokerIDByBank);
	getString(req, "BankSecuAcc", myreq.BankSecuAcc);
	getChar(req, "BankPwdFlag", &myreq.BankPwdFlag);
	getChar(req, "SecuPwdFlag", &myreq.SecuPwdFlag);
	getString(req, "OperNo", myreq.OperNo);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "TID", &myreq.TID);
	getChar(req, "TransferStatus", &myreq.TransferStatus);
	getString(req, "LongCustomerName", myreq.LongCustomerName);
	int i = this->api->ReqFromBankToFutureByFuture(&myreq, reqid);
	return i;
};

int TdApiApp::reqFromFutureToBankByFuture(const dict &req, int reqid)
{
	CThostFtdcReqTransferField myreq = CThostFtdcReqTransferField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradeCode", myreq.TradeCode);
	getString(req, "BankID", myreq.BankID);
	getString(req, "BankBranchID", myreq.BankBranchID);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "BrokerBranchID", myreq.BrokerBranchID);
	getString(req, "TradeDate", myreq.TradeDate);
	getString(req, "TradeTime", myreq.TradeTime);
	getString(req, "BankSerial", myreq.BankSerial);
	getString(req, "TradingDay", myreq.TradingDay);
	getInt(req, "PlateSerial", &myreq.PlateSerial);
	getChar(req, "LastFragment", &myreq.LastFragment);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "CustomerName", myreq.CustomerName);
	getChar(req, "IdCardType", &myreq.IdCardType);
	getString(req, "IdentifiedCardNo", myreq.IdentifiedCardNo);
	getChar(req, "CustType", &myreq.CustType);
	getString(req, "BankAccount", myreq.BankAccount);
	getString(req, "BankPassWord", myreq.BankPassWord);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "Password", myreq.Password);
	getInt(req, "InstallID", &myreq.InstallID);
	getInt(req, "FutureSerial", &myreq.FutureSerial);
	getString(req, "UserID", myreq.UserID);
	getChar(req, "VerifyCertNoFlag", &myreq.VerifyCertNoFlag);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getDouble(req, "TradeAmount", &myreq.TradeAmount);
	getDouble(req, "FutureFetchAmount", &myreq.FutureFetchAmount);
	getChar(req, "FeePayFlag", &myreq.FeePayFlag);
	getDouble(req, "CustFee", &myreq.CustFee);
	getDouble(req, "BrokerFee", &myreq.BrokerFee);
	getString(req, "Message", myreq.Message);
	getString(req, "Digest", myreq.Digest);
	getChar(req, "BankAccType", &myreq.BankAccType);
	getString(req, "DeviceID", myreq.DeviceID);
	getChar(req, "BankSecuAccType", &myreq.BankSecuAccType);
	getString(req, "BrokerIDByBank", myreq.BrokerIDByBank);
	getString(req, "BankSecuAcc", myreq.BankSecuAcc);
	getChar(req, "BankPwdFlag", &myreq.BankPwdFlag);
	getChar(req, "SecuPwdFlag", &myreq.SecuPwdFlag);
	getString(req, "OperNo", myreq.OperNo);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "TID", &myreq.TID);
	getChar(req, "TransferStatus", &myreq.TransferStatus);
	getString(req, "LongCustomerName", myreq.LongCustomerName);
	int i = this->api->ReqFromFutureToBankByFuture(&myreq, reqid);
	return i;
};

int TdApiApp::reqQueryBankAccountMoneyByFuture(const dict &req, int reqid)
{
	CThostFtdcReqQueryAccountField myreq = CThostFtdcReqQueryAccountField();
	memset(&myreq, 0, sizeof(myreq));
	getString(req, "TradeCode", myreq.TradeCode);
	getString(req, "BankID", myreq.BankID);
	getString(req, "BankBranchID", myreq.BankBranchID);
	getString(req, "BrokerID", myreq.BrokerID);
	getString(req, "BrokerBranchID", myreq.BrokerBranchID);
	getString(req, "TradeDate", myreq.TradeDate);
	getString(req, "TradeTime", myreq.TradeTime);
	getString(req, "BankSerial", myreq.BankSerial);
	getString(req, "TradingDay", myreq.TradingDay);
	getInt(req, "PlateSerial", &myreq.PlateSerial);
	getChar(req, "LastFragment", &myreq.LastFragment);
	getInt(req, "SessionID", &myreq.SessionID);
	getString(req, "CustomerName", myreq.CustomerName);
	getChar(req, "IdCardType", &myreq.IdCardType);
	getString(req, "IdentifiedCardNo", myreq.IdentifiedCardNo);
	getChar(req, "CustType", &myreq.CustType);
	getString(req, "BankAccount", myreq.BankAccount);
	getString(req, "BankPassWord", myreq.BankPassWord);
	getString(req, "AccountID", myreq.AccountID);
	getString(req, "Password", myreq.Password);
	getInt(req, "FutureSerial", &myreq.FutureSerial);
	getInt(req, "InstallID", &myreq.InstallID);
	getString(req, "UserID", myreq.UserID);
	getChar(req, "VerifyCertNoFlag", &myreq.VerifyCertNoFlag);
	getString(req, "CurrencyID", myreq.CurrencyID);
	getString(req, "Digest", myreq.Digest);
	getChar(req, "BankAccType", &myreq.BankAccType);
	getString(req, "DeviceID", myreq.DeviceID);
	getChar(req, "BankSecuAccType", &myreq.BankSecuAccType);
	getString(req, "BrokerIDByBank", myreq.BrokerIDByBank);
	getString(req, "BankSecuAcc", myreq.BankSecuAcc);
	getChar(req, "BankPwdFlag", &myreq.BankPwdFlag);
	getChar(req, "SecuPwdFlag", &myreq.SecuPwdFlag);
	getString(req, "OperNo", myreq.OperNo);
	getInt(req, "RequestID", &myreq.RequestID);
	getInt(req, "TID", &myreq.TID);
	getString(req, "LongCustomerName", myreq.LongCustomerName);
	int i = this->api->ReqQueryBankAccountMoneyByFuture(&myreq, reqid);
	return i;
};


///-------------------------------------------------------------------------------------
///Boost.Python封装
///-------------------------------------------------------------------------------------

class PyTdApiApp : public TdApiApp
{
public:
    using TdApiApp::TdApiApp;
    
	void onFrontConnected() override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onFrontConnected);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onFrontDisconnected(int reqid) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onFrontDisconnected, reqid);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onHeartBeatWarning(int reqid) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onHeartBeatWarning, reqid);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspAuthenticate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspAuthenticate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspUserLogin(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspUserLogin, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspUserLogout(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspUserLogout, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspUserPasswordUpdate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspUserPasswordUpdate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspTradingAccountPasswordUpdate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspTradingAccountPasswordUpdate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspUserAuthMethod(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspUserAuthMethod, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspGenUserCaptcha(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspGenUserCaptcha, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspGenUserText(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspGenUserText, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspOrderInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspOrderInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspParkedOrderInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspParkedOrderInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspParkedOrderAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspParkedOrderAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspOrderAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspOrderAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQueryMaxOrderVolume(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQueryMaxOrderVolume, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspSettlementInfoConfirm(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspSettlementInfoConfirm, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspRemoveParkedOrder(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspRemoveParkedOrder, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspRemoveParkedOrderAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspRemoveParkedOrderAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspExecOrderInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspExecOrderInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspExecOrderAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspExecOrderAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspForQuoteInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspForQuoteInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQuoteInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQuoteInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQuoteAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQuoteAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspBatchOrderAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspBatchOrderAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspOptionSelfCloseInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspOptionSelfCloseInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspOptionSelfCloseAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspOptionSelfCloseAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspCombActionInsert(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspCombActionInsert, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryOrder(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryOrder, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryTrade(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryTrade, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInvestorPosition(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInvestorPosition, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryTradingAccount(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryTradingAccount, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInvestor(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInvestor, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryTradingCode(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryTradingCode, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInstrumentMarginRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInstrumentMarginRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInstrumentCommissionRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInstrumentCommissionRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryExchange(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryExchange, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryProduct(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryProduct, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInstrument(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInstrument, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryDepthMarketData(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryDepthMarketData, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQrySettlementInfo(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQrySettlementInfo, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryTransferBank(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryTransferBank, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInvestorPositionDetail(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInvestorPositionDetail, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryNotice(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryNotice, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQrySettlementInfoConfirm(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQrySettlementInfoConfirm, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInvestorPositionCombineDetail(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInvestorPositionCombineDetail, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryCFMMCTradingAccountKey(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryCFMMCTradingAccountKey, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryEWarrantOffset(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryEWarrantOffset, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInvestorProductGroupMargin(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInvestorProductGroupMargin, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryExchangeMarginRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryExchangeMarginRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryExchangeMarginRateAdjust(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryExchangeMarginRateAdjust, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryExchangeRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryExchangeRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQrySecAgentACIDMap(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQrySecAgentACIDMap, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryProductExchRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryProductExchRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryProductGroup(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryProductGroup, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryMMInstrumentCommissionRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryMMInstrumentCommissionRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryMMOptionInstrCommRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryMMOptionInstrCommRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInstrumentOrderCommRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInstrumentOrderCommRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQrySecAgentTradingAccount(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQrySecAgentTradingAccount, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQrySecAgentCheckMode(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQrySecAgentCheckMode, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQrySecAgentTradeInfo(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQrySecAgentTradeInfo, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryOptionInstrTradeCost(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryOptionInstrTradeCost, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryOptionInstrCommRate(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryOptionInstrCommRate, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryExecOrder(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryExecOrder, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryForQuote(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryForQuote, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryQuote(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryQuote, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryOptionSelfClose(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryOptionSelfClose, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryInvestUnit(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryInvestUnit, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryCombInstrumentGuard(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryCombInstrumentGuard, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryCombAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryCombAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryTransferSerial(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryTransferSerial, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryAccountregister(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryAccountregister, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspError(const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspError, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnOrder(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnOrder, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnTrade(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnTrade, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnOrderInsert(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnOrderInsert, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnOrderAction(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnOrderAction, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnInstrumentStatus(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnInstrumentStatus, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnBulletin(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnBulletin, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnTradingNotice(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnTradingNotice, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnErrorConditionalOrder(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnErrorConditionalOrder, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnExecOrder(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnExecOrder, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnExecOrderInsert(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnExecOrderInsert, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnExecOrderAction(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnExecOrderAction, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnForQuoteInsert(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnForQuoteInsert, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnQuote(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnQuote, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnQuoteInsert(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnQuoteInsert, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnQuoteAction(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnQuoteAction, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnForQuoteRsp(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnForQuoteRsp, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnCFMMCTradingAccountToken(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnCFMMCTradingAccountToken, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnBatchOrderAction(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnBatchOrderAction, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnOptionSelfClose(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnOptionSelfClose, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnOptionSelfCloseInsert(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnOptionSelfCloseInsert, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnOptionSelfCloseAction(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnOptionSelfCloseAction, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnCombAction(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnCombAction, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnCombActionInsert(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnCombActionInsert, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryContractBank(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryContractBank, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryParkedOrder(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryParkedOrder, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryParkedOrderAction(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryParkedOrderAction, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryTradingNotice(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryTradingNotice, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryBrokerTradingParams(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryBrokerTradingParams, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQryBrokerTradingAlgos(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQryBrokerTradingAlgos, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQueryCFMMCTradingAccountToken(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQueryCFMMCTradingAccountToken, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnFromBankToFutureByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnFromBankToFutureByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnFromFutureToBankByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnFromFutureToBankByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnRepealFromBankToFutureByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnRepealFromBankToFutureByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnRepealFromFutureToBankByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnRepealFromFutureToBankByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnFromBankToFutureByFuture(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnFromBankToFutureByFuture, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnFromFutureToBankByFuture(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnFromFutureToBankByFuture, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnRepealFromBankToFutureByFutureManual(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnRepealFromBankToFutureByFutureManual, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnRepealFromFutureToBankByFutureManual(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnRepealFromFutureToBankByFutureManual, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnQueryBankBalanceByFuture(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnQueryBankBalanceByFuture, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnBankToFutureByFuture(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnBankToFutureByFuture, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnFutureToBankByFuture(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnFutureToBankByFuture, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnRepealBankToFutureByFutureManual(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnRepealBankToFutureByFutureManual, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnRepealFutureToBankByFutureManual(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnRepealFutureToBankByFutureManual, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onErrRtnQueryBankBalanceByFuture(const dict &data, const dict &error) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onErrRtnQueryBankBalanceByFuture, data, error);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnRepealFromBankToFutureByFuture(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnRepealFromBankToFutureByFuture, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnRepealFromFutureToBankByFuture(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnRepealFromFutureToBankByFuture, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspFromBankToFutureByFuture(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspFromBankToFutureByFuture, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspFromFutureToBankByFuture(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspFromFutureToBankByFuture, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRspQueryBankAccountMoneyByFuture(const dict &data, const dict &error, int reqid, bool last) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRspQueryBankAccountMoneyByFuture, data, error, reqid, last);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnOpenAccountByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnOpenAccountByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnCancelAccountByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnCancelAccountByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};

	void onRtnChangeAccountByBank(const dict &data) override
	{
		try
		{
			PYBIND11_OVERLOAD(void, TdApiApp, onRtnChangeAccountByBank, data);
		}
		catch (const error_already_set &e)
		{
			cout << e.what() << endl;
		}
	};


};


PYBIND11_MODULE(vnctptd_se, m)
{
    class_<TdApiApp, PyTdApiApp> TdApiApp(m, "TdApiApp");
    TdApiApp
        .def(init<>())
        .def("createFtdcTraderApi", &TdApiApp::createFtdcTraderApi)
        .def("release", &TdApiApp::release)
        .def("init", &TdApiApp::init)
        .def("join", &TdApiApp::join)
        .def("exit", &TdApiApp::exit)
        .def("getTradingDay", &TdApiApp::getTradingDay)
        .def("registerFront", &TdApiApp::registerFront)
        .def("subscribePublicTopic", &TdApiApp::subscribePublicTopic)
        .def("subscribePrivateTopic", &TdApiApp::subscribePrivateTopic)

		.def("reqAuthenticate", &TdApiApp::reqAuthenticate)
		.def("reqUserLogin", &TdApiApp::reqUserLogin)
		.def("reqUserLogout", &TdApiApp::reqUserLogout)
		.def("reqUserPasswordUpdate", &TdApiApp::reqUserPasswordUpdate)
		.def("reqTradingAccountPasswordUpdate", &TdApiApp::reqTradingAccountPasswordUpdate)
		.def("reqUserAuthMethod", &TdApiApp::reqUserAuthMethod)
		.def("reqGenUserCaptcha", &TdApiApp::reqGenUserCaptcha)
		.def("reqGenUserText", &TdApiApp::reqGenUserText)
		.def("reqUserLoginWithCaptcha", &TdApiApp::reqUserLoginWithCaptcha)
		.def("reqUserLoginWithText", &TdApiApp::reqUserLoginWithText)
		.def("reqUserLoginWithOTP", &TdApiApp::reqUserLoginWithOTP)
		.def("reqOrderInsert", &TdApiApp::reqOrderInsert)
		.def("reqParkedOrderInsert", &TdApiApp::reqParkedOrderInsert)
		.def("reqParkedOrderAction", &TdApiApp::reqParkedOrderAction)
		.def("reqOrderAction", &TdApiApp::reqOrderAction)
		.def("reqQueryMaxOrderVolume", &TdApiApp::reqQueryMaxOrderVolume)
		.def("reqSettlementInfoConfirm", &TdApiApp::reqSettlementInfoConfirm)
		.def("reqRemoveParkedOrder", &TdApiApp::reqRemoveParkedOrder)
		.def("reqRemoveParkedOrderAction", &TdApiApp::reqRemoveParkedOrderAction)
		.def("reqExecOrderInsert", &TdApiApp::reqExecOrderInsert)
		.def("reqExecOrderAction", &TdApiApp::reqExecOrderAction)
		.def("reqForQuoteInsert", &TdApiApp::reqForQuoteInsert)
		.def("reqQuoteInsert", &TdApiApp::reqQuoteInsert)
		.def("reqQuoteAction", &TdApiApp::reqQuoteAction)
		.def("reqBatchOrderAction", &TdApiApp::reqBatchOrderAction)
		.def("reqOptionSelfCloseInsert", &TdApiApp::reqOptionSelfCloseInsert)
		.def("reqOptionSelfCloseAction", &TdApiApp::reqOptionSelfCloseAction)
		.def("reqCombActionInsert", &TdApiApp::reqCombActionInsert)
		.def("reqQryOrder", &TdApiApp::reqQryOrder)
		.def("reqQryTrade", &TdApiApp::reqQryTrade)
		.def("reqQryInvestorPosition", &TdApiApp::reqQryInvestorPosition)
		.def("reqQryTradingAccount", &TdApiApp::reqQryTradingAccount)
		.def("reqQryInvestor", &TdApiApp::reqQryInvestor)
		.def("reqQryTradingCode", &TdApiApp::reqQryTradingCode)
		.def("reqQryInstrumentMarginRate", &TdApiApp::reqQryInstrumentMarginRate)
		.def("reqQryInstrumentCommissionRate", &TdApiApp::reqQryInstrumentCommissionRate)
		.def("reqQryExchange", &TdApiApp::reqQryExchange)
		.def("reqQryProduct", &TdApiApp::reqQryProduct)
		.def("reqQryInstrument", &TdApiApp::reqQryInstrument)
		.def("reqQryDepthMarketData", &TdApiApp::reqQryDepthMarketData)
		.def("reqQrySettlementInfo", &TdApiApp::reqQrySettlementInfo)
		.def("reqQryTransferBank", &TdApiApp::reqQryTransferBank)
		.def("reqQryInvestorPositionDetail", &TdApiApp::reqQryInvestorPositionDetail)
		.def("reqQryNotice", &TdApiApp::reqQryNotice)
		.def("reqQrySettlementInfoConfirm", &TdApiApp::reqQrySettlementInfoConfirm)
		.def("reqQryInvestorPositionCombineDetail", &TdApiApp::reqQryInvestorPositionCombineDetail)
		.def("reqQryCFMMCTradingAccountKey", &TdApiApp::reqQryCFMMCTradingAccountKey)
		.def("reqQryEWarrantOffset", &TdApiApp::reqQryEWarrantOffset)
		.def("reqQryInvestorProductGroupMargin", &TdApiApp::reqQryInvestorProductGroupMargin)
		.def("reqQryExchangeMarginRate", &TdApiApp::reqQryExchangeMarginRate)
		.def("reqQryExchangeMarginRateAdjust", &TdApiApp::reqQryExchangeMarginRateAdjust)
		.def("reqQryExchangeRate", &TdApiApp::reqQryExchangeRate)
		.def("reqQrySecAgentACIDMap", &TdApiApp::reqQrySecAgentACIDMap)
		.def("reqQryProductExchRate", &TdApiApp::reqQryProductExchRate)
		.def("reqQryProductGroup", &TdApiApp::reqQryProductGroup)
		.def("reqQryMMInstrumentCommissionRate", &TdApiApp::reqQryMMInstrumentCommissionRate)
		.def("reqQryMMOptionInstrCommRate", &TdApiApp::reqQryMMOptionInstrCommRate)
		.def("reqQryInstrumentOrderCommRate", &TdApiApp::reqQryInstrumentOrderCommRate)
		.def("reqQrySecAgentTradingAccount", &TdApiApp::reqQrySecAgentTradingAccount)
		.def("reqQrySecAgentCheckMode", &TdApiApp::reqQrySecAgentCheckMode)
		.def("reqQrySecAgentTradeInfo", &TdApiApp::reqQrySecAgentTradeInfo)
		.def("reqQryOptionInstrTradeCost", &TdApiApp::reqQryOptionInstrTradeCost)
		.def("reqQryOptionInstrCommRate", &TdApiApp::reqQryOptionInstrCommRate)
		.def("reqQryExecOrder", &TdApiApp::reqQryExecOrder)
		.def("reqQryForQuote", &TdApiApp::reqQryForQuote)
		.def("reqQryQuote", &TdApiApp::reqQryQuote)
		.def("reqQryOptionSelfClose", &TdApiApp::reqQryOptionSelfClose)
		.def("reqQryInvestUnit", &TdApiApp::reqQryInvestUnit)
		.def("reqQryCombInstrumentGuard", &TdApiApp::reqQryCombInstrumentGuard)
		.def("reqQryCombAction", &TdApiApp::reqQryCombAction)
		.def("reqQryTransferSerial", &TdApiApp::reqQryTransferSerial)
		.def("reqQryAccountregister", &TdApiApp::reqQryAccountregister)
		.def("reqQryContractBank", &TdApiApp::reqQryContractBank)
		.def("reqQryParkedOrder", &TdApiApp::reqQryParkedOrder)
		.def("reqQryParkedOrderAction", &TdApiApp::reqQryParkedOrderAction)
		.def("reqQryTradingNotice", &TdApiApp::reqQryTradingNotice)
		.def("reqQryBrokerTradingParams", &TdApiApp::reqQryBrokerTradingParams)
		.def("reqQryBrokerTradingAlgos", &TdApiApp::reqQryBrokerTradingAlgos)
		.def("reqQueryCFMMCTradingAccountToken", &TdApiApp::reqQueryCFMMCTradingAccountToken)
		.def("reqFromBankToFutureByFuture", &TdApiApp::reqFromBankToFutureByFuture)
		.def("reqFromFutureToBankByFuture", &TdApiApp::reqFromFutureToBankByFuture)
		.def("reqQueryBankAccountMoneyByFuture", &TdApiApp::reqQueryBankAccountMoneyByFuture)

		.def("onFrontConnected", &TdApiApp::onFrontConnected)
		.def("onFrontDisconnected", &TdApiApp::onFrontDisconnected)
		.def("onHeartBeatWarning", &TdApiApp::onHeartBeatWarning)
		.def("onRspAuthenticate", &TdApiApp::onRspAuthenticate)
		.def("onRspUserLogin", &TdApiApp::onRspUserLogin)
		.def("onRspUserLogout", &TdApiApp::onRspUserLogout)
		.def("onRspUserPasswordUpdate", &TdApiApp::onRspUserPasswordUpdate)
		.def("onRspTradingAccountPasswordUpdate", &TdApiApp::onRspTradingAccountPasswordUpdate)
		.def("onRspUserAuthMethod", &TdApiApp::onRspUserAuthMethod)
		.def("onRspGenUserCaptcha", &TdApiApp::onRspGenUserCaptcha)
		.def("onRspGenUserText", &TdApiApp::onRspGenUserText)
		.def("onRspOrderInsert", &TdApiApp::onRspOrderInsert)
		.def("onRspParkedOrderInsert", &TdApiApp::onRspParkedOrderInsert)
		.def("onRspParkedOrderAction", &TdApiApp::onRspParkedOrderAction)
		.def("onRspOrderAction", &TdApiApp::onRspOrderAction)
		.def("onRspQueryMaxOrderVolume", &TdApiApp::onRspQueryMaxOrderVolume)
		.def("onRspSettlementInfoConfirm", &TdApiApp::onRspSettlementInfoConfirm)
		.def("onRspRemoveParkedOrder", &TdApiApp::onRspRemoveParkedOrder)
		.def("onRspRemoveParkedOrderAction", &TdApiApp::onRspRemoveParkedOrderAction)
		.def("onRspExecOrderInsert", &TdApiApp::onRspExecOrderInsert)
		.def("onRspExecOrderAction", &TdApiApp::onRspExecOrderAction)
		.def("onRspForQuoteInsert", &TdApiApp::onRspForQuoteInsert)
		.def("onRspQuoteInsert", &TdApiApp::onRspQuoteInsert)
		.def("onRspQuoteAction", &TdApiApp::onRspQuoteAction)
		.def("onRspBatchOrderAction", &TdApiApp::onRspBatchOrderAction)
		.def("onRspOptionSelfCloseInsert", &TdApiApp::onRspOptionSelfCloseInsert)
		.def("onRspOptionSelfCloseAction", &TdApiApp::onRspOptionSelfCloseAction)
		.def("onRspCombActionInsert", &TdApiApp::onRspCombActionInsert)
		.def("onRspQryOrder", &TdApiApp::onRspQryOrder)
		.def("onRspQryTrade", &TdApiApp::onRspQryTrade)
		.def("onRspQryInvestorPosition", &TdApiApp::onRspQryInvestorPosition)
		.def("onRspQryTradingAccount", &TdApiApp::onRspQryTradingAccount)
		.def("onRspQryInvestor", &TdApiApp::onRspQryInvestor)
		.def("onRspQryTradingCode", &TdApiApp::onRspQryTradingCode)
		.def("onRspQryInstrumentMarginRate", &TdApiApp::onRspQryInstrumentMarginRate)
		.def("onRspQryInstrumentCommissionRate", &TdApiApp::onRspQryInstrumentCommissionRate)
		.def("onRspQryExchange", &TdApiApp::onRspQryExchange)
		.def("onRspQryProduct", &TdApiApp::onRspQryProduct)
		.def("onRspQryInstrument", &TdApiApp::onRspQryInstrument)
		.def("onRspQryDepthMarketData", &TdApiApp::onRspQryDepthMarketData)
		.def("onRspQrySettlementInfo", &TdApiApp::onRspQrySettlementInfo)
		.def("onRspQryTransferBank", &TdApiApp::onRspQryTransferBank)
		.def("onRspQryInvestorPositionDetail", &TdApiApp::onRspQryInvestorPositionDetail)
		.def("onRspQryNotice", &TdApiApp::onRspQryNotice)
		.def("onRspQrySettlementInfoConfirm", &TdApiApp::onRspQrySettlementInfoConfirm)
		.def("onRspQryInvestorPositionCombineDetail", &TdApiApp::onRspQryInvestorPositionCombineDetail)
		.def("onRspQryCFMMCTradingAccountKey", &TdApiApp::onRspQryCFMMCTradingAccountKey)
		.def("onRspQryEWarrantOffset", &TdApiApp::onRspQryEWarrantOffset)
		.def("onRspQryInvestorProductGroupMargin", &TdApiApp::onRspQryInvestorProductGroupMargin)
		.def("onRspQryExchangeMarginRate", &TdApiApp::onRspQryExchangeMarginRate)
		.def("onRspQryExchangeMarginRateAdjust", &TdApiApp::onRspQryExchangeMarginRateAdjust)
		.def("onRspQryExchangeRate", &TdApiApp::onRspQryExchangeRate)
		.def("onRspQrySecAgentACIDMap", &TdApiApp::onRspQrySecAgentACIDMap)
		.def("onRspQryProductExchRate", &TdApiApp::onRspQryProductExchRate)
		.def("onRspQryProductGroup", &TdApiApp::onRspQryProductGroup)
		.def("onRspQryMMInstrumentCommissionRate", &TdApiApp::onRspQryMMInstrumentCommissionRate)
		.def("onRspQryMMOptionInstrCommRate", &TdApiApp::onRspQryMMOptionInstrCommRate)
		.def("onRspQryInstrumentOrderCommRate", &TdApiApp::onRspQryInstrumentOrderCommRate)
		.def("onRspQrySecAgentTradingAccount", &TdApiApp::onRspQrySecAgentTradingAccount)
		.def("onRspQrySecAgentCheckMode", &TdApiApp::onRspQrySecAgentCheckMode)
		.def("onRspQrySecAgentTradeInfo", &TdApiApp::onRspQrySecAgentTradeInfo)
		.def("onRspQryOptionInstrTradeCost", &TdApiApp::onRspQryOptionInstrTradeCost)
		.def("onRspQryOptionInstrCommRate", &TdApiApp::onRspQryOptionInstrCommRate)
		.def("onRspQryExecOrder", &TdApiApp::onRspQryExecOrder)
		.def("onRspQryForQuote", &TdApiApp::onRspQryForQuote)
		.def("onRspQryQuote", &TdApiApp::onRspQryQuote)
		.def("onRspQryOptionSelfClose", &TdApiApp::onRspQryOptionSelfClose)
		.def("onRspQryInvestUnit", &TdApiApp::onRspQryInvestUnit)
		.def("onRspQryCombInstrumentGuard", &TdApiApp::onRspQryCombInstrumentGuard)
		.def("onRspQryCombAction", &TdApiApp::onRspQryCombAction)
		.def("onRspQryTransferSerial", &TdApiApp::onRspQryTransferSerial)
		.def("onRspQryAccountregister", &TdApiApp::onRspQryAccountregister)
		.def("onRspError", &TdApiApp::onRspError)
		.def("onRtnOrder", &TdApiApp::onRtnOrder)
		.def("onRtnTrade", &TdApiApp::onRtnTrade)
		.def("onErrRtnOrderInsert", &TdApiApp::onErrRtnOrderInsert)
		.def("onErrRtnOrderAction", &TdApiApp::onErrRtnOrderAction)
		.def("onRtnInstrumentStatus", &TdApiApp::onRtnInstrumentStatus)
		.def("onRtnBulletin", &TdApiApp::onRtnBulletin)
		.def("onRtnTradingNotice", &TdApiApp::onRtnTradingNotice)
		.def("onRtnErrorConditionalOrder", &TdApiApp::onRtnErrorConditionalOrder)
		.def("onRtnExecOrder", &TdApiApp::onRtnExecOrder)
		.def("onErrRtnExecOrderInsert", &TdApiApp::onErrRtnExecOrderInsert)
		.def("onErrRtnExecOrderAction", &TdApiApp::onErrRtnExecOrderAction)
		.def("onErrRtnForQuoteInsert", &TdApiApp::onErrRtnForQuoteInsert)
		.def("onRtnQuote", &TdApiApp::onRtnQuote)
		.def("onErrRtnQuoteInsert", &TdApiApp::onErrRtnQuoteInsert)
		.def("onErrRtnQuoteAction", &TdApiApp::onErrRtnQuoteAction)
		.def("onRtnForQuoteRsp", &TdApiApp::onRtnForQuoteRsp)
		.def("onRtnCFMMCTradingAccountToken", &TdApiApp::onRtnCFMMCTradingAccountToken)
		.def("onErrRtnBatchOrderAction", &TdApiApp::onErrRtnBatchOrderAction)
		.def("onRtnOptionSelfClose", &TdApiApp::onRtnOptionSelfClose)
		.def("onErrRtnOptionSelfCloseInsert", &TdApiApp::onErrRtnOptionSelfCloseInsert)
		.def("onErrRtnOptionSelfCloseAction", &TdApiApp::onErrRtnOptionSelfCloseAction)
		.def("onRtnCombAction", &TdApiApp::onRtnCombAction)
		.def("onErrRtnCombActionInsert", &TdApiApp::onErrRtnCombActionInsert)
		.def("onRspQryContractBank", &TdApiApp::onRspQryContractBank)
		.def("onRspQryParkedOrder", &TdApiApp::onRspQryParkedOrder)
		.def("onRspQryParkedOrderAction", &TdApiApp::onRspQryParkedOrderAction)
		.def("onRspQryTradingNotice", &TdApiApp::onRspQryTradingNotice)
		.def("onRspQryBrokerTradingParams", &TdApiApp::onRspQryBrokerTradingParams)
		.def("onRspQryBrokerTradingAlgos", &TdApiApp::onRspQryBrokerTradingAlgos)
		.def("onRspQueryCFMMCTradingAccountToken", &TdApiApp::onRspQueryCFMMCTradingAccountToken)
		.def("onRtnFromBankToFutureByBank", &TdApiApp::onRtnFromBankToFutureByBank)
		.def("onRtnFromFutureToBankByBank", &TdApiApp::onRtnFromFutureToBankByBank)
		.def("onRtnRepealFromBankToFutureByBank", &TdApiApp::onRtnRepealFromBankToFutureByBank)
		.def("onRtnRepealFromFutureToBankByBank", &TdApiApp::onRtnRepealFromFutureToBankByBank)
		.def("onRtnFromBankToFutureByFuture", &TdApiApp::onRtnFromBankToFutureByFuture)
		.def("onRtnFromFutureToBankByFuture", &TdApiApp::onRtnFromFutureToBankByFuture)
		.def("onRtnRepealFromBankToFutureByFutureManual", &TdApiApp::onRtnRepealFromBankToFutureByFutureManual)
		.def("onRtnRepealFromFutureToBankByFutureManual", &TdApiApp::onRtnRepealFromFutureToBankByFutureManual)
		.def("onRtnQueryBankBalanceByFuture", &TdApiApp::onRtnQueryBankBalanceByFuture)
		.def("onErrRtnBankToFutureByFuture", &TdApiApp::onErrRtnBankToFutureByFuture)
		.def("onErrRtnFutureToBankByFuture", &TdApiApp::onErrRtnFutureToBankByFuture)
		.def("onErrRtnRepealBankToFutureByFutureManual", &TdApiApp::onErrRtnRepealBankToFutureByFutureManual)
		.def("onErrRtnRepealFutureToBankByFutureManual", &TdApiApp::onErrRtnRepealFutureToBankByFutureManual)
		.def("onErrRtnQueryBankBalanceByFuture", &TdApiApp::onErrRtnQueryBankBalanceByFuture)
		.def("onRtnRepealFromBankToFutureByFuture", &TdApiApp::onRtnRepealFromBankToFutureByFuture)
		.def("onRtnRepealFromFutureToBankByFuture", &TdApiApp::onRtnRepealFromFutureToBankByFuture)
		.def("onRspFromBankToFutureByFuture", &TdApiApp::onRspFromBankToFutureByFuture)
		.def("onRspFromFutureToBankByFuture", &TdApiApp::onRspFromFutureToBankByFuture)
		.def("onRspQueryBankAccountMoneyByFuture", &TdApiApp::onRspQueryBankAccountMoneyByFuture)
		.def("onRtnOpenAccountByBank", &TdApiApp::onRtnOpenAccountByBank)
		.def("onRtnCancelAccountByBank", &TdApiApp::onRtnCancelAccountByBank)
		.def("onRtnChangeAccountByBank", &TdApiApp::onRtnChangeAccountByBank)
		;
}
